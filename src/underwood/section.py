"""Provide class that returns sections of our HTML document.

This class handles the logic of creating each section of the HTML
document, e.g. the top of the document.
"""

from string import Template

from underwood.file import File


class Section:
    """Define a base class for sections of the HTML document."""

    def __init__(self, info: dict, page: dict) -> None:
        """Initialize the section object.

        Args:
            info: our JSON info containing metadata about our blog
            page: (or post) containing info about the page we are making
        """
        self.info = info
        self.page = page  # This can be used for pages or posts.


class Top(Section):
    """Define a class that gets the top section of the HTML document."""

    # fmt: off
    _template = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$domain_name | $title</title>
</head>
<style>
html {
    font-size: 1.25em;
    line-height: 1.25;
    margin: auto;
    max-width: 70ch;
}
</style>
<body> 
<h1>$domain_name</h1>
<nav>
$nav_links
</nav>
<hr/>
<div><i>$description</i></div>
<hr/>\n""")
    # fmt: on

    def _nav_links(self) -> str:
        """Return a set of links for each page specified in blog info.

        This is essentially the "navbar" for the blog.
        """
        pages = self.info["pages"]
        nav_links = ""
        for idx, page in enumerate(pages):
            at_end = idx == len(pages) - 1
            if at_end:
                nav_links += f"<a href=\"{page['file']}\">{page['title']}</a>"
            else:
                nav_links += f"<a href=\"{page['file']}\">{page['title']}</a> | "
        return nav_links

    def contents(self) -> str:
        """Return the top of the HTML document.

        This is the head tag along with its contents, the opening body
        tag, and whatever else we want at the top of each page or post.
        """
        return self._template.substitute(
            domain_name=self.info["domain_name"],
            title=self.page["title"],
            description=self.page["description"],
            nav_links=self._nav_links(),
        )


class Middle(Section):
    """Define a class that gets the middle of the HTML document."""

    def contents(self) -> str:
        """Return the middle section of the HTML document.

        This is the stuff we want to sandwich between the body tags.
        """
        path = f"{self.info['input_dir']}/{self.page['file']}"
        file = File(path)
        return file.read()


class Bottom(Section):
    """Define a class that gets the bottom of the HTML document."""

    # fmt: off
    _template = """<hr/>
<footer>
<a href="#">Back to the top</a>
</footer>
</body>
</html>"""
    # fmt: on

    def contents(self) -> str:
        """Return the bottom section of the HTML document."""
        return self._template
