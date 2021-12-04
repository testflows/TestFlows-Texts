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
import sys
import testflows._core.cli.arg.type as argtype

from textwrap import dedent

from testflows._core.cli.arg.common import epilog
from testflows._core.cli.arg.common import HelpFormatter
from testflows._core.cli.arg.handlers.handler import Handler as HandlerBase
from testflows._core.funcs import current

from .core import Document
from .executable import execute


class Handler(HandlerBase):
    @classmethod
    def add_command(cls, commands):
        parser = commands.add_parser("run", help="run executable document", epilog=epilog(),
            description=(dedent("""
            Run executable document.
            
            Specify '--' at the end of the command line options to pass
            options to the writer program.

            For example:
               tfs document run <input> <output> -- --help

            Set PYTHONPATH when modules needed by the executable
            document are not in the default path.

            For example:
               PYTHONPATH=<path/to/module> tfs document run <input> <output>

            """).strip()),
            formatter_class=HelpFormatter)

        parser.add_argument("input", metavar="input", type=argtype.file("r", bufsize=1, encoding="utf-8"),
                            help="input file, use '-' for stdin")
        parser.add_argument("output", metavar="output", type=argtype.file("w", bufsize=1, encoding="utf-8"),
                            help='output file')

        parser.set_defaults(func=cls())

    def handle(self, args):
        name = str(args.input.name)
        if name == "<stdin>":
            name = "document"

        with Document(name):
            current().context.file = args.output
            execute(source=args.input)
