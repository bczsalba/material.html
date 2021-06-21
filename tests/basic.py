from os.path import abspath, dirname
from material import (
    Document,
    Header,
    Div,
    Img,
    home_text,
    home_image,
    lorem_ipsum,
    tag,
)


def create_documents():
    """Create all sites"""

    jeremy = home_image(
        Img(
            cls="content-img",
            src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages6.alphacoders.com%2F678%2F678636.jpg",
        )
    )

    with Document("site/index.html") as doc:
        doc.styles["accent"] = "#8c7bb7"

        content = doc.add_content()
        content.elements.append(
            home_text(
                (
                    tag("h1", inner="This is Jeremy."),
                    tag("h2", inner="say hi to Jeremny!"),
                    tag("p", inner="Dogs are cute."),
                )
            )
        )

        content.elements.append(jeremy)
        doc.write_supporting_to("./site/")

    with Document("site/first.html") as doc:
        doc.contents.append(jeremy)

    with Document("site/second.html") as doc:
        doc.contents.append(jeremy)

    with Document("site/third.html") as doc:
        doc.contents.append(jeremy)


def main():
    """Setup data & create documents"""

    header = Header()
    header.set_branding(tag("i", cls="fas fa-dog"))
    header.add_tab("first", href="first.html", inner=tag("span", inner="First").value)
    header.add_tab("second", href="second.html", inner=tag("span", inner="Second").value)
    header.add_tab("third", href="third.html", inner=tag("span", inner="Third").value)
    header.add_tab_icon("language", onclick="toggleLanguage()")
    header.add_tab_icon(
        "dark_mode", subclass="outlined", ID="dark-mode-toggle", onclick="toggleDark()"
    )

    Document.global_header = header
    create_documents()


if __name__ == "__main__":
    main()
