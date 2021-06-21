"""
material.objects.
-----------------

author: bczsalba
"""

# pylint: disable=invalid-name

from __future__ import annotations


from shutil import copyfile
from typing import Optional, Any
from dataclasses import dataclass, field
from os.path import dirname, abspath, join

from html5print import HTMLBeautifier

from .templates import (
    DIV_TEMPLATE,
    IMG_TEMPLATE,
    DOCUMENT_TEMPLATE,
    HEADER_TEMPLATE,
    TAB_TEMPLATE,
    TAB_ICON_TEMPLATE,
)


@dataclass
class HtmlElement:
    """Base class for all elements defined below"""

    cls: str = ""
    ID: str = ""


@dataclass
class Custom(HtmlElement):
    """Element that allows setting custom html code
    Note: be sure to use `Content(value=...)`"""

    value: str = ""


@dataclass
class Div(HtmlElement):
    """Representative of the HTML div tag
    Modify its elements using `Div().elements`"""

    elements: list[HtmlElement] = field(default_factory=list)

    @property
    def value(self) -> str:
        """Return HTML of object"""

        return DIV_TEMPLATE.format(
            cls=self.cls,
            ID=self.ID,
            elements="\n".join(element.value for element in self.elements),
        )


@dataclass
class Img(HtmlElement):
    """Representative of the HTML img tag"""

    src: str = ""
    alt: str = ""

    @property
    def value(self) -> str:
        """Return HTML of object"""

        return IMG_TEMPLATE.format(
            src=self.src,
            alt=self.alt,
            cls=self.cls,
            ID=self.ID,
        )


class Header:
    """Material (mdc) header class for Document"""

    def __init__(self) -> None:
        """Initialize object"""

        self.branding = ""
        self.tabs: list[str] = []
        self.icons: list[str] = []
        self.value = ""

    def _set_value(self) -> None:
        """Update HTML of object"""

        self.value = HEADER_TEMPLATE.format(
            branding=self.branding,
            tabs="\n".join(line for line in self.tabs),
            icons="\n".join(line for line in self.icons),
        )

    def set_branding(self, tag: str) -> None:
        """Set left-hand-side branding"""

        self.branding = tag
        self._set_value()

    def add_tab(
        self, name: str, href: Optional[str] = None, inner: Optional[str] = None
    ) -> None:
        """Add a new textual tab element"""

        if href is None:
            href = f"{name}.html"

        if inner is None:
            inner = f"<span>{name}</span>"

        self.tabs.append(TAB_TEMPLATE.format(href=href, inner=inner, name=name))
        self._set_value()

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
        self._set_value()


class Document:
    """Representative of an HTML file (document)"""

    global_header: Optional[Header] = None

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

                for key, value in self.styles.items():
                    css = css.replace("{" + key + "}", value)

                style.write(css)

        copyfile(join(supporting_dir, "index.js"), join(target_dir, "index.js"))
