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
from testflows.core import *
from testflows._core.test import TestDecorator
from testflows._core.testtype import TestSubType

TextStep = TestStep
TextOutline = TestOutline
TextBackground = TestBackground
TextModule = TestModule

triple_quotes = '"""'

class Book(Module):
    def __new__(cls, name=None, **kwargs):
        kwargs["subtype"] = TestSubType.Book
        return super(Book, cls).__new__(cls, name, **kwargs)

class Chapter(Suite):
    def __new__(cls, name=None, **kwargs):
        kwargs["subtype"] = TestSubType.Chapter
        return super(Chapter, cls).__new__(cls, name, **kwargs)

class Document(Test):
    def __new__(cls, name=None, **kwargs):
        kwargs["subtype"] = TestSubType.Document
        return super(Document, cls).__new__(cls, name, **kwargs)

class Page(Test):
    def __new__(cls, name=None, **kwargs):
        kwargs["subtype"] = TestSubType.Page
        return super(Page, cls).__new__(cls, name, **kwargs)

class Section(Test):
    def __new__(cls, name=None, **kwargs):
        kwargs["subtype"] = TestSubType.Section
        return super(Section, cls).__new__(cls, name, **kwargs)

class Paragraph(Step):
    def __new__(cls, name=None, **kwargs):
        kwargs["subtype"] = TestSubType.Paragraph
        return super(Paragraph, cls).__new__(cls, name, **kwargs)

class TextBook(TestDecorator):
    type = Book

class TextChapter(TestDecorator):
    type = Chapter

class TextDocument(TestDecorator):
    type = Document

class TextPage(TestDecorator):
    type = Page

class TextSection(TestDecorator):
    type = Section

class TextParagraph(TestDecorator):
    type = Paragraph
    subtype = None
