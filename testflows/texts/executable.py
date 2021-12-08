# Copyright 2021 Katteli Inc.
# TestFlows.com Open-Source Software Testing Framework (http://testflows.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
import inspect

from textwrap import indent, dedent
from tempfile import NamedTemporaryFile
from linecache import cache as code_cache
from contextlib import ExitStack

from testflows._core.contrib.arpeggio import RegExMatch as _
from testflows._core.contrib.arpeggio import OneOrMore, ZeroOrMore, EOF, Optional, Not
from testflows._core.contrib.arpeggio import ParserPython as PEGParser
from testflows._core.contrib.arpeggio import PTNodeVisitor, visit_parse_tree
from testflows._core.exceptions import exception as get_exception

from testflows.texts import *

DummySection = NullStep

class TestStack(ExitStack):
    def push_context(self, cm):
        return super(TestStack, self).enter_context(cm)

    def pop_context(self):
        """Pop and close last context manager from stack.
        """
        is_sync, cb = self._exit_callbacks.pop()
        assert is_sync
        cb(None, None, None)


class Visitor(PTNodeVisitor):
    def __init__(self, stack, source_data, *args, **kwargs):
        self.stack = stack
        self.source_data = source_data
        self.globals = globals()
        self.locals = {}
        self.current_level = 0
        super(Visitor, self).__init__(*args, **kwargs)

    def visit_header(self, node, children):
        self.process(node)

    def execute(visitor, node):
        visitor.locals["self"] = current()

        position = node.position
        lines = node.flat_str()

        if node.rule_name == "exec_code":
            exec_lines = "\n".join(lines.strip().splitlines()[1:-1])
        else:
            if lines.endswith('"'):
                end = lines.rsplit('"')[-1]
                exec_lines = fr'''text(fr"""{lines}""", dedent=False, end='{end}')'''
            else:
                exec_lines = f'text(fr"""{lines}""", dedent=False, end="")'

        with NamedTemporaryFile("w+", suffix=".py") as code_file:
            code_file.write(exec_lines)
            code_file.seek(0)
            code_file.flush()
            visitor.locals["__file__"] = code_file.name

            source_code = code_file.read()
            source_name = code_file.name
    
            code_cache[source_name] = (
                len(source_code), None,
                [line+'\n' for line in source_code.splitlines()], source_name
            )

            try:
                exec(compile(source_code, source_name, 'exec'),
                        visitor.globals, visitor.locals)   
            except Exception as e:
                exc_tb = e.__traceback__
                syntax_error = isinstance(e, SyntaxError)

                if syntax_error:
                    tb_lineno = e.lineno
                else:
                    exc_tb = exc_tb.tb_next
                    tb_lineno = exc_tb.tb_lineno
        
                split_lines = lines.splitlines()

                code_offset = 0
                if node.rule_name == "exec_code":
                    code_offset = 1
                line_offset = visitor.source_data[:position].count("\n")

                line_fmt = "  %" + str(len(str(len(split_lines) + line_offset))) + "d|  %s"
                line_at_fmt = "  %" + str(len(str(len(split_lines) + line_offset))) + "d|> %s"

                numbered_lines = "\n".join(
                    [line_fmt % (n + line_offset,l) if n != tb_lineno + code_offset else line_at_fmt % (n + line_offset,l) for n, l in enumerate(
                        split_lines, 1)])

                code_exc = type(e)(str(e) + f"\n\n{'Syntax Error' if syntax_error else 'Error'} occured in the following text:\n\n"
                        + numbered_lines)

                code_exc.with_traceback(exc_tb)
                err(f"{e.__class__.__name__}\n" + get_exception(type(e), code_exc, code_exc.__traceback__))

    def process(self, node):
        for child in node:
            self.execute(child)

    def visit_intro(self, node, children):
        self.process(node)

    def visit_section(self, node, children):
        section_level = node[0].value.count("#")
        
        assert self.current_level >= 0, "current level is invalid"
        
        section = Section(node.heading.heading_name.value.strip(), context=SharedContext(current().context))

        if section_level > self.current_level:
            for i in range(section_level - self.current_level - 1):
                self.stack.push_context(DummySection())
        else:
            for i in range(self.current_level - section_level + 1):
                self.stack.pop_context()

        self.stack.push_context(section)
        self.current_level = section_level
        self.process(node)


def Parser():
    """TestFlows executable document parser.
    """
    def line():
        return _(r"[^\n]*\n")
    
    def non_empty_line():
        return _(r"[^\n]+\n")

    def final_line():
        return _(r"[^\n]+"), EOF

    def paragraph():
        return OneOrMore(Not(exec_code_start), [non_empty_line, final_line])

    def header_sep():
        return _(r"---[ \t]*\n")

    def header():
        return header_sep, ZeroOrMore(Not(header_sep), line), header_sep

    def exec_code_start():
        return _(r"[ \t]?[ \t]?[ \t]?[`~][`~][`~]python:testflows[ \t]*\n")
    
    def exec_code_end():
        return (_(r"[ \t]?[ \t]?[ \t]?[`~][`~][`~][ \t]*"), [_(r"\n"), EOF])

    def exec_code():
        return exec_code_start, ZeroOrMore(Not(exec_code_end), line), exec_code_end

    def intro():
        return ZeroOrMore(Not(heading), [exec_code, paragraph, line, final_line])

    def section():
        return heading, ZeroOrMore(Not(heading), [exec_code, paragraph, line, final_line])

    def heading():
        return [
            (_(r"\s*#+\s+"), heading_name, _(r"\n?")),
            (heading_name, _(r"\n?[-=]+\n?"))
        ]

    def heading_name():
        return _(r"[^\n]+")

    def document():
        return Optional(Optional(header), intro, ZeroOrMore(section))

    return PEGParser(document, skipws=False)


def execute(source):
    """Execute TestFlows Document (*.tfd).

    :param source: source file-like object
    """
    parser = Parser()
    source_data = source.read()
    
    if not source_data:
        fail(f"source file '{os.path.abspath(source.name)}' is empty")
    
    tree = parser.parse(source_data)

    if tree is None:
        err(f"parsing {os.path.abspath(source.name)} failed")

    with TestStack() as stack:
        visit_parse_tree(tree, Visitor(stack, source_data))
