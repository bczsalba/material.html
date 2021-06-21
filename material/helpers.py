"""
material.objects.
-----------------

author: bczsalba
"""

from .objects import Div, Img, Custom, HtmlElement


def home_text(content: HtmlElement) -> Div:
    """Get div of class home-text with given content"""

    return Div(cls="home-text", elements=[content])


def home_image(content: Img) -> Div:
    """Get div of class home-image with given content"""

    return Div(cls="home-image", elements=[content])


def lorem_ipsum() -> Div:
    """Return placeholder lorem ipsum text div"""

    return home_text(
        Custom(
            value="""\
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vestibulum, nulla ut lobortis rutrum, quam ante suscipit mi, sed aliquet elit nulla vel magna. Cras fermentum eros vehicula ex pretium, sit amet fringilla enim aliquam. Pellentesque maximus feugiat augue vel tempor. Vestibulum sed sapien consectetur, lobortis libero eu, rutrum odio. In in sapien consequat, ornare erat in, commodo leo. Nunc ornare sed dui id gravida. Mauris sed ipsum vitae mi pretium euismod in vel tellus. Fusce interdum lacinia scelerisque. Integer nisi ex, dignissim at interdum malesuada, rhoncus a risus. Duis eget facilisis nisl. Suspendisse rutrum laoreet nisl in pulvinar. Vestibulum molestie lacinia augue ut finibus. Vestibulum sodales dictum scelerisque. Maecenas tristique nec risus a scelerisque.
                Ut at finibus sapien. Morbi ipsum felis, egestas in volutpat eget, tempor accumsan quam. Mauris sed dictum erat. Sed vehicula ante vel mattis congue. Nunc et neque mollis, pulvinar dui in, efficitur lectus. Proin sed elit eu enim aliquam cursus non in turpis. Curabitur sit amet tempus ante. Pellentesque id est ac tellus viverra pharetra. Aliquam eu fermentum augue. Donec in lorem id eros ultricies feugiat. Nullam tempor volutpat tortor quis convallis. Integer vel ex tempor, cursus dolor sit amet, placerat urna. Maecenas vehicula ex vel dolor venenatis interdum. In non bibendum elit.
            </p>
        """
        )
    )
