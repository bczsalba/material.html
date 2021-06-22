"""
material.objects
----------------
author: bczsalba


All the HTML elements for this module.
"""

# pylint: disable=invalid-name

from __future__ import annotations


from shutil import copyfile
from datetime import datetime
from typing import Optional, Any
from dataclasses import dataclass, field
from os.path import dirname, abspath, join

from html5print import HTMLBeautifier

from .templates import (
    DOCUMENT_TEMPLATE,
    HEADER_TEMPLATE,
    TAB_TEMPLATE,
    TAB_ICON_TEMPLATE,
)


@dataclass
class HtmlElement:
    """Base class for all HTML tags"""

    cls: str = ""
    ID: str = ""

    name: str = field(default="", init=False)
    _inner: str = field(init=False)

    def __post_init__(self) -> None:
        setattr(self, "_inner", "")

    @property
    def tag_data(self) -> str:
        """Get data for tag (the stuff in the starting tag)"""

        data = ""
        for key in getattr(self, "__dataclass_fields__").keys():
            if key.startswith("_") or key == "name":
                continue

            value = getattr(self, key)

            if key == "ID":
                key = "id"

            elif key == "cls":
                key = "class"

            if len(value) > 0 and isinstance(value, str):
                data += f" {key}=\"{value}\""

        return data

    @property
    def inner(self) -> str:
        """Return self._field"""

        return self._inner

    @property
    def value(self) -> str:
        """Return HTML of HtmlElement"""

        return (
            self.start_tag() + self.inner + self.end_tag()
        )

    def start_tag(self) -> str:
        """Get starting tag value"""

        return "<" + self.name + self.tag_data + ">"

    def end_tag(self) -> str:
        """Get end tag value"""

        return f"</{self.name}>"


def tag(name, inner: str = "", **html_args) -> HtmlElement:
    """Create a custom tag"""

    obj = HtmlElement(**html_args)
    obj.name = name
    setattr(obj, "_inner", inner)

    return obj
        
@dataclass
class Div(HtmlElement):
    """Representative of the HTML div tag
    Modify its elements using `Div().elements`"""

    name = "div"
    elements: list[HtmlElement] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Set up custom HtmlElement"""

        self.tagtype = "div"

    @property
    def inner(self) -> str:
        """Get inner value for tag"""

        return "\n".join(element.value for element in self.elements)


@dataclass
class Img(HtmlElement):
    """Representative of the HTML img tag"""

    name = "img"
    src: str = ""
    alt: str = ""


class Header:
    """Material (mdc) header class for Document"""

    def __init__(self) -> None:
        """Initialize object"""

        self.branding = ""
        self.tabs: list[str] = []
        self.icons: list[str] = []

    @property
    def value(self) -> str:
        """Get HTML of object"""

        return HEADER_TEMPLATE.format(
            branding=self.branding.value,
            tabs="\n".join(line for line in self.tabs),
            icons="\n".join(line for line in self.icons),
        )

    def set_branding(self, tag: HtmlElement) -> None:
        """Set left-hand-side branding"""

        self.branding = tag

    def add_tab(
        self, name: str, href: Optional[str] = None, inner: Optional[str] = None
    ) -> None:
        """Add a new textual tab element

        Note: `inner` for now has to be a string!"""

        if href is None:
            href = f"{name}.html"

        if inner is None:
            inner = f"<span>{name}</span>"

        self.tabs.append(TAB_TEMPLATE.format(href=href, inner=inner, name=name))

    def add_tab_icon(
        self, icon: str, ID: str = "", onclick: str = "", subclass: str = ""
    ) -> None:
        """Add a new icon tab element"""

        if subclass != "":
            subclass = "-" + subclass

        self.icons.append(
            TAB_ICON_TEMPLATE.format(
                icon=icon, ID=ID, onclick=onclick, subclass=subclass
            )
        )


class Document:
    """Representative of an HTML file (document)"""

    global_header: Optional[Header] = None
    global_include_css: list[str] = []

    def __init__(self, filename: str) -> None:
        """Initialize object"""

        self.title = "WIP"
        self.filename = filename
        self.contents: list[Div] = []

        if Document.global_header is None:
            header = Header()
        else:
            header = Document.global_header

        self.header: Header = header
        self.name = filename.split("/")[-1].split(".")[0]

        self.styles = {
            "accent": "orange",
            "foreground": "var(--accent)",
            "background": "#ffffff",
            "header-one": "#000000",
            "header-two": "#666666",
            "paragraph": "#888888",
            "layer-first": "#212121",
            "dark-background": "#1d1d1d",
            "dark-header-one": "#ddd",
            "dark-header-two": "#bbb",
            "dark-paragraph": "#888",
        }

    @property
    def value(self) -> Any:
        """Return beautified HTML of object"""

        return HTMLBeautifier.beautify(
            DOCUMENT_TEMPLATE.format(
                name=self.name,
                title=self.title,
                header=("" if self.header is None else self.header.value),
                contents="\n".join(content.value for content in self.contents),
                include_css="\n".join(f'<link rel="stylesheet" href="{src}">' for src in Document.global_include_css),
            ),
            indent=4,
        )

    def __enter__(self) -> Document:
        """Enter context"""

        return self

    def __exit__(self, *args: tuple[Any]) -> None:
        """Exit context, write to file"""

        self.write(self.filename)
        print("Generated", self.name, "at", self.filename)

    def add_content(self) -> Div:
        """Add a new Div with class="content", return it"""

        self.contents.append(Div(cls="content"))
        return self.contents[-1]

    def write(self, filename: str) -> None:
        """Write document HTML to a filename"""

        with open(filename, "w") as file:
            file.write(self.value)

    def write_supporting_to(self, name: Optional[str] = None) -> None:
        """Write supporting data (CSS, JS) to some directory"""

        supporting_dir = join(dirname(abspath(__file__)), "supporting")

        if name is None:
            target_dir = abspath(self.filename)
        else:
            target_dir = abspath(name)

        with open(join(supporting_dir, "template.css"), "r") as template:
            with open(join(target_dir, "style.css"), "w") as style:
                header_width = str(100 / len(self.header.tabs)) + "%"
                css = template.read().replace("{width}", header_width)
                css = css.replace("{time}", format(datetime.now(), "%Y-%m-%d %H:%M%:%S"))

                for key, value in self.styles.items():
                    css = css.replace("{" + key + "}", value)

                style.write(css)

        copyfile(join(supporting_dir, "index.js"), join(target_dir, "index.js"))
