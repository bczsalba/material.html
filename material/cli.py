"""
material.cli
------------
author: bczsalba


This module provides an easy to access utility to generate
websites from simple markup. At the moment it is constrained
to the most useful subset of the features material.html
provides, but that is to change depending on needs. The CLI
currently uses YAML as it's expected filetype, but expanding to
JSON should be pretty simple in the future.

Note: The generator part of this module can be used programatically:
```python3
from material import create_documents

# JSON / Python object containing same information format as below
website_data: dict[str, Any] = ...

create_documents(website_data)
```

The basic structure of the file is as follows:

```yaml
config:
    # Set root folder for all Document-s
    root: .

    # Edit branding
    branding:
        # Select type of branding, icon/image. Icon type uses fontawesome
        type: str
        # Image link or fontawesome class name of selected branding
        value: str

    # Edit icon visibility
    icons:
        dark_mode: false
        language: false

    # Edit the Document.styles dictionary
    styles:
        accent: "#669420

pages:
    Page Title:
        navname:
            en: Name of navigation item
            hu: Same thing in Hungarian

        card_0:
            title:
                en: This is the first card
                hu: Same thing in Hungarian

            body:
                en: This is some sample body text
                hu: Same thing in Hungarian

            images:
                - link/to/static/image.png
                - [link/to/anchor/image.jpg, link/to/anchor.html]

        card_1:
            ...

        card_nothing_after_card_matters:
            ...

    Other Page Title:
        ...
"""


from __future__ import annotations

import sys
from os import chdir
from typing import Any
from argparse import ArgumentParser, Namespace

import yaml
from material import Header, Document, tag, Img, Div, Anchor


def load_config(data: dict[str, Any], header: Header) -> None:
    """Load config options"""

    for key, value in data.items():
        if key == "root":
            chdir(value)
            continue

        if key == "icons":
            for icon_name, should_use in value.items():
                if not should_use:
                    continue

                if icon_name == "dark_mode":
                    header.add_tab_icon(
                        "dark_mode",
                        onclick="toggleDark()",
                        subclass="outlined",
                        ID="dark-mode-toggle",
                    )

                elif icon_name == "language":
                    header.add_tab_icon(
                        "language",
                        onclick="toggleLanguage()",
                        subclass="outlined",
                        ID="language-toggle",
                    )

        if key == "styles":
            for s_key, s_value in value.items():
                Document.styles[s_key] = s_value

        if key == "branding":
            if value["type"] == "image":
                header.set_branding(Img(src=value["value"]))
                continue

            if value["type"] == "icon":
                header.set_branding(tag("i", cls="fas " + value["value"]))


def create_page(name: str, title: str, content: dict[str, Any]) -> None:
    """Create page with title & content"""

    with Document(name) as page:
        page.write_supporting_to(".")
        page.title = title

        for i, (key, value) in enumerate(content.items()):
            if not key.startswith("card"):
                continue

            div = page.add_content()
            texts = []
            images = []

            for i_key, i_value in value.items():
                if i_key == "title":
                    for lang, translation in i_value.items():
                        texts.append(tag("h1", translation, cls=lang))
                    continue

                if i_key == "body":
                    for lang, translation in i_value.items():
                        texts.append(tag("p", translation, cls=lang))
                    continue

                if i_key == "images":
                    for src in i_value:
                        if isinstance(src, list):
                            src, href = src
                            anchor = Anchor(href=href)
                            anchor.elements.append(Img(src=src, cls="clickable"))
                            images.append(anchor)
                            continue

                        images.append(Img(src=src))

            # Change order for each image
            actions = [
                lambda div=div, texts=texts: div.elements.append(
                    Div(cls="home-text", elements=texts)
                ),
                lambda div=div, images=images: div.elements.append(
                    Div(cls="home-image", elements=images)
                ),
            ]

            if len(images) == 0:
                actions[0]()
                continue

            if len(texts) == 0:
                actions[1]()
                continue

            actions[1 - i % 2]()
            actions[i % 2]()

    return page


def create_documents(data: dict[str, Any], root: str | None = None) -> None:
    """Create documents from loaded data"""

    header = Header()
    Document.global_header = header

    if root is not None:
        data["config"]["root"] = root

    if data.get("config") is not None:
        load_config(data["config"], header=header)

    tab_tmpl = "<span class={lang}>{value}</span>"

    for title, content in data["pages"].items():
        navnames = content["navname"]
        tab_content = ""
        for lang, navname in navnames.items():
            if navname == "index.html":
                continue

            tab_content += tab_tmpl.format(value=navname, lang=lang)

        if len(tab_content) > 0:
            header.add_tab(
                navnames["en"],
                href=navnames["en"],
                inner=tab_content,
            )

    for title, content in data["pages"].items():
        navname = content["navname"]["en"]
        create_page(navname, title, content)


def parse_arguments(args: list[str]) -> Namespace:
    """Parse all arguments passed as a list"""

    parser = ArgumentParser()
    parser.add_argument("file", help="YAML file to use as generator base")
    parser.add_argument("-o", "--output", help="output directory. overrides `root`")

    if len(args) == 0:
        parser.print_help()
        return None

    return parser.parse_args()


def main() -> None:
    """Main method"""

    args = parse_arguments(sys.argv[1:])
    if args is None:
        return

    with open(args.file, "r", encoding="utf-8") as file:
        content = yaml.safe_load(file)

    create_documents(content, root=args.output)


if __name__ == "__main__":
    main()
