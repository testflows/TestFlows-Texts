from testflows.texts import *

@TextParagraph
def paragraph(self):
    with Paragraph("paragraph"):
        pass

@TextSection
def section(self):
    with Section("section"):
        pass

@TextPage
def page(self):
    with Page("page"):
        pass

@TextDocument
def document(self):
    with Document("document"):
        pass

@TextChapter
def chapter(self):
    with Chapter("chapter"):
        pass

@TextOutline(Page)
def outline(self):
    pass

@TextBackground
def background(self):
    pass

@TextBook
def book(self):
    Chapter(run=chapter)
    Document(run=document)
    Page(run=page)
    Section(run=section)
    Paragraph(run=paragraph)
    Outline(run=outline)
    outline()
    Background(run=background)

if main():
    book()
