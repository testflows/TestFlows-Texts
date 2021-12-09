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

Follow the example Markdown document to get to know how you can write auto verified docs yourself.

```markdown
    ## This is a heading

    This file is written using Markdown where you can have any number
    of `python:testflows` code block that contain executable Python code.
    
    ```python:testflows
    # This is Python code that will be executed when .tfd document is run.
    msg = "Hello TestFlows Texts"
    ```
 
    The scope is shared between all the code blocks in the same document.
    
    ```python:testflows
    # `msg` variable is can now be accessed in any following `python:testflows` blocks
    
    new_msg = msg + " Thanks for making verifying docs so easy!"
    ```
    
    The output of running `.tfd` document is the final `.md` file
    with all the `python:testflows` code blocks removed and replaced with any
    text added to the document using the `text()` function.

    ```python:testflows
    # Let's use `text()` function to add some text to our document
    # dynamically in our Python code.
 
    text("add this line to the final Markdown document")
    ```
```

