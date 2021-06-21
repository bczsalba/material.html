from os.path import abspath, dirname
from material import (
    Document,
    Header,
    Div,
    Img,
    Custom,
    home_text,
    home_image,
    lorem_ipsum,
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
                Custom(
                    value="""\
                    <h1>This is Jeremy.</h1>
                    <h2>say hi to Jeremy!</h2>
                    <p>Dogs are cute.</p>
                """
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
    header.set_branding("<span class='logo'><i class='fas fa-dog'></i></span>")
    header.add_tab("first", href="first.html", inner=f"<span>First</span>")
    header.add_tab("second", href="second.html", inner=f"<span>Second</span>")
    header.add_tab("third", href="third.html", inner=f"<span>Third</span>")
    header.add_tab_icon("language", onclick="toggleLanguage()")
    header.add_tab_icon(
        "dark_mode", subclass="outlined", ID="dark-mode-toggle", onclick="toggleDark()"
    )

    Document.global_header = header
    create_documents()


if __name__ == "__main__":
    main()
