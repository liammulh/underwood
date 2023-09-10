"""Provides a dataclass that defines templates for our HTML document.

These templates require content to be substituted into them. There
is another class that uses these templates to create sections of an
HTML document.
"""

import dataclasses
from string import Template


@dataclasses.dataclass
class HTMLTemplate:
    """Defines string templates for our HTML documents.

    Attributes:
        top: amongst other things, HTML head and opening body tag
        link: anchor tag template
        post_summary: we display a summaries of posts on the home page
        archive: comprehensive list of posts by date or tag
        bottom: footer and closing tags
    """

    # fmt: off
    top = Template("""<!DOCTYPE html>
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

    details = Template("""<details style="$style">
<summary>
$summary
</summary>
$contents
</details>\n""")

    link = Template('<a href="$href">$text</a>')

    post_summary = Template("""<h2>$post_title_link</h2>
<i>$pretty_date</i>
<p>
$description $read_more_link
</p>\n""")

    archive = """<details>
<summary>Browse by date</summary>
</details>
<details>
<summary>Browse by tag</summary>
</details>"""

    bottom = """<hr/>
<footer>
<a href="#">Back to the top</a>
</footer>
</body>
</html>"""
    # fmt: on
