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
import os
import sys
import testflows._core.cli.arg.type as argtype

from textwrap import dedent

from testflows._core.cli.arg.common import epilog
from testflows._core.cli.arg.common import HelpFormatter
from testflows._core.cli.arg.handlers.handler import Handler as HandlerBase
from testflows._core.funcs import current
from testflows._core.test import NullStep

from .core import Document, Module, err
from .executable import execute


class Handler(HandlerBase):
    @classmethod
    def add_command(cls, commands):
        parser = commands.add_parser("run", help="run executable document", epilog=epilog(),
            description=(dedent("""
            Run executable document.

            Executable documents are Markdown documents that
            contain `python:testflows` code blocks which may contain
            any Python code that will be run during document execution.  

            All text within executable document except for the
            `python:testflows` code blocks are treated as Python f-strings.
            Therefore, you must escape any `{`, `}` characters by doubling
            them, for example: `{{` or `}}`, otherwise they will be treated
            as f-string expressions.

            Text must not contain triple quotes `\"\"\"`. If you need them
            then you must use `text()` function within `python:testflows` code block
            to explicitly add them to the the text. 

            For example:
                ```python:testflows
                text('adding triple quotes \"\"\" to text')
                ``` 

            Specify '--' at the end of the command line options to pass
            options to the executable document writer program itself.

            For example:
               tfs document run -i <path> -o <path> -- --help

            You must set PYTHONPATH when modules needed by the executable
            document are not in the default path.

            For example:
               PYTHONPATH=<path/to/module> tfs document run -i <path> -o <path>

            The `--input` can take multiple files and in such case if `--output`
            is specified it is treated as directory name.

            For example,
               tfs document run -i `find $(pwd) -name "*.tfd"` -o . -f 
            or
               tfs document run -i `find $(pwd) -name "*.tfd"` -o /path/to/output/dir -f 
            
            If input is '-' (stdin) and output is '.' then output file is 'document.md'
            which is created in the current working directory.
            """).strip()),
            formatter_class=HelpFormatter)

        parser.add_argument("-i", "--input", metavar="path", type=argtype.file("r", bufsize=1, encoding="utf-8"),
                            nargs="+", help="input file, use '-' for stdin, default: stdin", default="-")
        parser.add_argument("-o", "--output", metavar="path", type=str, nargs="?",
                            help=('output file or directory if multiple input files are passed,\n'
                                  'default: \'.\' or if input is stdin then \'-\'.\n'
                                  'The \'.\' means to create output file in the same directory as the input\n'
                                  'file having .md extension and the \'-\' means output to stdout.'), default="")
        parser.add_argument("-f", "--force", action="store_true",
                            help="force to override existing output file if it already exists", default=False)

        parser.set_defaults(func=cls())

    def handle(self, args):
        if type(args.input) not in (list, tuple):
            args.input = [args.input]

        with Module("documents") if len(args.input) > 1 else NullStep():
            relative_directory = ""
    
            for doc in args.input:
                output = args.output
                
                if len(args.input) > 1:
                    commondir = os.path.commonpath([i.name for i in args.input])
                    relative_directory, filename = os.path.split(os.path.relpath(doc.name, commondir))

                if not output:
                    if doc.name == "<stdin>":
                        output = "-"
                    else:
                        output = "."

                elif len(args.input) > 1:
                    directory = os.path.join(output, relative_directory)
                    os.makedirs(directory, exist_ok=True)                  
                    output = os.path.join(directory, "".join(filename.rsplit(".", 1)[:1] + [".md"]))

                if output == ".":
                    if doc.name == "<stdin>":
                        output = "document.md"
                    else:
                        directory, filename = os.path.split(doc.name)
                        output = os.path.join(directory, "".join(filename.rsplit(".", 1)[:1] + [".md"]))

                if output == doc.name:
                    if current():
                        err("output file '{output}'is the same as input file")
                    else:
                        raise ValueError("output file can't be the same as input file") 

                if os.path.exists(output) and not args.force:
                    if current():
                        err(f"output file '{output}' already exists")
                    else:
                        raise ValueError(f"output file '{output}' already exists")

                output = argtype.file("w", bufsize=1, encoding="utf-8")(output)

                if output.name == "<stdout>":
                    sys.argv += ["--output", "quiet"]

                try:
                    with Document(os.path.join(relative_directory, os.path.basename(doc.name) if doc.name != "<stdin>" else "document")):
                        current().context.file = output
                        execute(source=doc)
                finally:
                    output.flush()
