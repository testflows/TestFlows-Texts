# TestFlows-Texts
TestFlows.com Open-Source Software Testing Framework Texts

Use `testflows.texts` Python module for writing auto verified software documentation
by combining text with the verification procedure of the
described functionality in the same source file.

Source files for auto verified documentation by convention have `.tfd` extension
and are written using Markdown. Therefore, all `.tfd` files are valid
Markdown files however `.tfd` files are only the source files for your documentation
that must be executed using `tfs document run` command to produce final 
Markdown documentation files.

```bash
$ tfs document run --input my_document.tfd --output my_document.md
```

## Requirements

* Python3 >= 3.8

## Install

You can install `testflows.texts` using `pip3` command:

```bash
pip3 install --upgrade testflows.texts
```

## Writing Auto Verified Docs

The documentation source file are written in Markdown with the `python:testflows`
code blocks embedded in the document that define any Python code that gets 
executed during the execution documentation source file using the `tfs document run`
command.

```markdown
    ## This is a heading

    This file is written using Markdown.

    The following `python:testflows` block will be removed
    from the final Markdown document where you can add any text from the Python
    code to the document using `text()` function. 

    ```python:testflows
    # This is executable Python code
    text("add this line to the final Markdown document")
    ```
```

