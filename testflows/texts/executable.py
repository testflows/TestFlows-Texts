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

from testflows._core.contrib.arpeggio import RegExMatch as _
from testflows._core.contrib.arpeggio import OneOrMore, ZeroOrMore, EOF, Optional, Not
from testflows._core.contrib.arpeggio import ParserPython as PEGParser
from testflows._core.contrib.arpeggio import PTNodeVisitor, visit_parse_tree

from testflows.texts import *


class Visitor(PTNodeVisitor):
    def __init__(self, *args, **kwargs):
        self.current_test = None
        self.globals = globals()
        self.locals = {}
        super(Visitor, self).__init__(*args, **kwargs)

    def visit_header(self, node, children):
        with Section("header"):
            lines = node.flat_str()
            text(lines, dedent=False, end="")

    def process_intro_or_section(visitor, node):
        visitor.locals["self"] = current()
        for child in node:
            lines = child.flat_str()
            if child.rule_name == "exec_code":
                with NamedTemporaryFile("w+", suffix=".py") as code_file:
                    code_file.write(
                        "\n".join(lines.strip().splitlines()[1:-1])
                    )
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
                        exc_tb= e.__traceback__.tb_next
                        split_lines = dedent(lines.strip()).splitlines()
                        line_fmt = "  %" + str(len(str(len(split_lines)))) + "d|  %s"
                        line_at_fmt = "  %" + str(len(str(len(split_lines)))) + "d|> %s"
                        numbered_lines = "\n".join(
                            [line_fmt % (n,l) if n != exc_tb.tb_lineno else line_at_fmt % (n,l) for n, l in enumerate(
                                split_lines)])
                        code_exc = type(e)(str(e) + "\n\nCode block (in document):\n"
                             + numbered_lines)
                        code_exc.with_traceback(exc_tb)
                        raise code_exc from None

            else:
                text(lines, dedent=False, end="")

    def visit_intro(self, node, children):
        self.process_intro_or_section(node)

    def visit_section(self, node, children):
        with Section(node.heading.heading_name.value.strip()):
            self.process_intro_or_section(node)



def Parser():
    """TestFlows executable document parser.
    """
    def line():
        return _(r"[^\n]*\n")

    def header_sep():
        return _(r"---\s*?\n")

    def header():
        return header_sep, ZeroOrMore(Not(header_sep), line), header_sep

    def exec_code_start():
        return _(r"\s?\s?\s?[`~][`~][`~]python:testflows\s*?\n")
    
    def exec_code_end():
        return _(r"\s?\s?\s?[`~][`~][`~]\s*?\n")

    def exec_code():
        return exec_code_start, ZeroOrMore(Not(exec_code_end), line), exec_code_end

    def intro():
        return ZeroOrMore(Not(heading), [exec_code, line])

    def section():
        return heading, ZeroOrMore(Not(heading), [exec_code, line])

    def heading():
        return [
            (_(r"\s*#+\s+"), heading_name, _(r"\n?")),
            (heading_name, _(r"\n?[-=]+\n?"))
        ]

    def heading_name():
        return _(r"[^\n]+")

    def document():
        return Optional(header, intro, ZeroOrMore(section)), EOF

    return PEGParser(document, skipws=False)


def execute(source):
    """Execute TestFlows Document (*.tfd).

    :param source: source file-like object
    """
    parser = Parser()
    source_data = source.read()
    tree = parser.parse(source_data)

    visit_parse_tree(tree, Visitor())
