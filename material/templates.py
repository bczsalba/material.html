"""
material.templates
------------------
author: bczsalba


Template strings for various tags.
Note: The CSS template is stored at supporting/template.css.
"""

__all__ = [
    "DIV_TEMPLATE",
    "IMG_TEMPLATE",
    "DOCUMENT_TEMPLATE",
    "HEADER_TEMPLATE",
    "TAB_TEMPLATE",
    "TAB_ICON_TEMPLATE",
]


DOCUMENT_TEMPLATE = """\
<!DOCTYPE html>
<html>
    <head>
        <title>{title}</title>
        <meta content="initial-scale=1, width=device-width" name="viewport">
        <meta charset="UTF-8">

        <link rel="preconnect" href="https://fonts.gstatic.com"> 
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons+Outlined">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.3/css/all.css" integrity="sha384-SZXxX4whJ79/gErwcOYf+zWLeJdY/qpuqC4cAa9rOGUstPomtqpuNWT9wdPEn2fk" crossorigin="anonymous">
        <link rel="stylesheet" href="style.css">
    </head>
    {header}
    <div class="content-parent" id="content-parent">
        {contents}
    </div>

    <!-- This is here because some divs need to load before it can execute -->
    <script src="index.js"></script>

    <!-- Set the right tab indicator to active: The first item in the comparison is formatted during generation -->
    <script>
        if ("{name}" != "index") {{
            document.getElementById("{name}-indicator").classList.add("active")
        }};
    </script>
</html>
"""

HEADER_TEMPLATE = """\
    <header class="header">
        <div class="header-branding">
            <a class="nav-item logo" title="Go home" href="./index.html">
                {branding}
            </a>
        </div>
        <div class="header-nav">
            <nav class="nav">
                {tabs}
            </nav>
            <div class="nav-icon">
                {icons}
            </div>
        </span>
    </header>
"""

TAB_TEMPLATE = """\
<a class="nav-item" href="{href}">
    {inner}
    <span class="nav-indicator" id="{name}-indicator">
</a>
"""

TAB_ICON_TEMPLATE = """\
<button class="material-icons{subclass} nav-item" id="{ID}" onclick="{onclick}">
    {icon}
</button>
"""
