"""Define a class that returns special pages in the blog.

As of this writing, the home page (index.html) and the archive page
are treated specially. With other pages, we just grab the source and
sandwich it between the top and bottom sections.
"""

from string import Template
from datetime import datetime as dt

from src.underwood.config import Config


def pretty_date(iso_8601_date: str) -> str:
    """Return a date whose format is: Thursday, January 1, 1970.

    Args:
        iso_8601_date: date with format yyyy-mm-dd
    """
    date_obj = dt.strptime(iso_8601_date, "%Y-%m-%d")
    weekday_and_month = date_obj.strftime("%A, %B ")
    day = date_obj.strftime("%d").lstrip("0") + ", "
    year = date_obj.strftime("%Y")
    return weekday_and_month + day + year


class Page:
    """Define the base class for a page."""
    def __init__(self, info: str) -> None:
        """Initialize the page object with the info provided."""
        self.info = info

    _link_template = Template('<a href="$href">$text</a>')


class Home(Page):
    """Define a class that gets the home page."""

    # fmt: off
    _post_summary_template = Template("""<h2>$post_title_link</h2>
<i>$pretty_date</i>
<p>
$description $read_more_link
</p>\n""")
    # fmt: on

    def get(self):
        """Return the contents of the home page (index.html).

        The home page contains a summary of the most recent posts from
        most to least recent. There is a global variable that can be
        configured that determines the number of posts on the home page.
        """
        home = ""
        posts = self.info["posts"]
        num_posts_to_show = (
            Config.NUM_POSTS_ON_HOME_PAGE.value
            if len(posts) > Config.NUM_POSTS_ON_HOME_PAGE.value
            else len(posts)
        )
        # Loop backwards so previous and next links make more sense.
        for idx, post in enumerate(reversed(posts)):
            if idx + 1 <= num_posts_to_show:
                post_title_link = self._link_template.substitute(
                    href=post["file"], text=post["title"]
                )
                read_more_link = self._link_template.substitute(
                    href=post["file"], text="Read more..."
                )
                home += self._post_summary_template.substitute(
                    post_title_link=post_title_link,
                    pretty_date=pretty_date(post["published"]),
                    description=post["description"],
                    read_more_link=read_more_link,
                )
        return home
