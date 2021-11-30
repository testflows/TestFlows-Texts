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
__author__ = "Vitaliy Zakaznikov"
__version__ = "1.7.__VERSION__"
__license__ = f"""
Copyright 2021 Katteli Inc.
TestFlows.com Open-Source Software Testing Framework (http://testflows.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
"""
import os
import sys

from testflows.connect import Shell
from testflows.asserts import error, errors

from .core import *

__all__ = [
        "os", "sys",
        "Shell", "error", "errors",
        "TextBook", "TextChapter", "TextDocument", "TextPage", "TextSection", "TextParagraph",
        "TextBackground", "TextOutline",
        "Book", "Chapter", "Document", "Page", "Section", "Paragraph", "Background", "Example", "Outline",
        "Context",
        "config",
        "NullStep",
        "Given", "When", "Then", "And", "But", "By", "Finally",
        "loads", "ordered", "retry", "retries",
        "has",
        "Flags",
        "OK", "XOK", "Fail", "XFail", "Skip", "Error", "XError", "Null", "XNull",
        "Name", "Description", "Uid", "Tags", "Args", "Setup", "Parallel", "Executor",
        "XFails", "XFlags", "Repeats", "Repeat", "Retries", "Retry", "Onlys", "Skips",
        "OnlyTags", "SkipTags",
        "FFails", "Skipped", "Failed", "XFailed", "XErrored", "Okayed", "XOkayed",
        "Attributes", "Requirements", "Specifications", "Examples", "ArgumentParser",
        "Node", "Tag", "Argument", "Attribute", "Requirement", "Specification", "Metric", "Value", "Ticket",
        "Secret",
        "Table",
        "The",
        "load", "append_path",
        "main", "args", "private_key",
        "metric", "ticket", "value", "note", "debug", "trace", "text",
        "attribute", "requirement", "tag",
        "input", "current_time",
        "message", "exception", "ok", "fail", "skip", "err",
        "result", "null", "xok", "xfail", "xerr", "xnull", "pause", "getsattr",
        "current_dir", "current_module", "load_module",
        "TE", "UT", "SKIP", "EOK", "EFAIL", "EERROR", "ESKIP",
        "XOK", "XFAIL", "XERROR", "XNULL",
        "FAIL_NOT_COUNTED", "ERROR_NOT_COUNTED", "NULL_NOT_COUNTED",
        "PAUSE", "PAUSE_BEFORE", "PAUSE_AFTER", "REPORT", "DOCUMENT", "MANUAL", "AUTO",
        "MANDATORY", "CLEAR", "NOT_REPEATABLE",
        "EANY", "ERESULT", "XRESULT",
        "PARALLEL", "NO_PARALLEL",
        "__author__", "__version__", "__license__",
        "join", "top", "current", "previous",
        "Pool", "ThreadPool", "SharedThreadPool",
        "AsyncPool", "SharedAsyncPool",
        "parallel",
        "objects",
        "name",
        "utils",
        "rsa"
    ]
