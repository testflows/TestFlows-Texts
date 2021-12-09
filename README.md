# TestFlows-Texts
TestFlows.com Open-Source Software Testing Framework Texts

Use `testflows.texts` Python module to help you write auto verified software documentation
by combining your text with the verification procedure of the described functionality
in the same source file while leveraging the power and flexibility of [TestFlows.com Open-Source Test Framework](https://testflows.com).

Source files for auto verified documentation by convention have `.tfd` extension
and are written using Markdown. Therefore, all `.tfd` files are valid
Markdown files. However, `.tfd` files are only the source files for your documentation
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

After installing `testflows.texts` you will also have `tfs` command available in your environment.

## Writing Auto Verified Docs

Follow the example Markdown document to get to know how you can write auto verified docs yourself.

```markdown
    ## This is a heading

    This file is written using Markdown where you can have any number
    of `python:testflows` code blocks that contain executable Python code.
    
    ```python:testflows
    # This is Python code that will be executed when .tfd document is run.
    
    msg = "Hello TestFlows Texts"
    ```
 
    The scope is shared between all the code blocks in the same document.
    
    ```python:testflows
    # so `msg` variable define above can also be accessed in this
    # `python:testflows` code block

    new_msg = msg + " Thanks for making verifying docs so easy!"
    ```
    
    The output of executing `.tfd` document using `tfs document run`
    is the final `.md` file with all the `python:testflows` code blocks
    removed and replaced with the text added to the document using
    the `text()` function.

    ```python:testflows
    # Let's use `text()` function to add some text to our document
    # dynamically in our Python code
 
    text("add this line to the final Markdown document")
    ```
    
    Any text outside the `python:testflows` code blocks are treated as Python
    f-strings. This allows you to specify expressions for substitutions.
    See [Python formatted string literals](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)
    for more details.
    
    Here is an example where we will substitute the value of `msg` variable next {msg}.
    But with Python f-strings you can specify even complex expressions. For example, we can 
    convert our string in `msg` to title case as follows {msg.title()}.
    
    You can double your curly braces to escape them when substitution expression is not needed
    using `{{` or `}}`.
    
    By the way, your document can't contain any triple double quotes `"""`. If you need them then you have to
    add them inside the `python:testflows` code block using `text()` function. For example,
    
    ```python:testflows
    text('"""')
    ```
    
    Well, this is pretty much it. With `testflows.texts` you have full power of full featured
    test framework and Python language at your disposal to make sure your documentation always
    stays to date.
```

