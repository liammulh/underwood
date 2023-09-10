"""Define a class that returns the middle section of pages in the blog.

As of this writing, the home page (index.html) and the archive page
are treated specially. With posts, we add some extra info and links.
With other pages, we just grab the source and sandwich it between the
top and bottom sections.
"""

from string import Template
from datetime import datetime as dt

from src.underwood.config import Config


class Page:
    """Define the base class for a page."""
    def __init__(self, info: str) -> None:
        """Initialize the page object with the info provided."""
        self.info = info

    _link_template = Template('<a href="$href">$text</a>')


class Home(Page):
    """Define a class that gets the home page's middle section."""

    # fmt: off
    _post_summary_template = Template("""<h2>$post_title_link</h2>
<i>$pretty_date</i>
<p>
$description $read_more_link
</p>\n""")
    # fmt: on

    @staticmethod
    def _pretty_date(iso_8601_date: str) -> str:
        """Return a date whose format is: Thursday, January 1, 1970.

        Args:
            iso_8601_date: date with format yyyy-mm-dd
        """
        date_obj = dt.strptime(iso_8601_date, "%Y-%m-%d")
        weekday_and_month = date_obj.strftime("%A, %B ")
        day = date_obj.strftime("%d").lstrip("0") + ", "
        year = date_obj.strftime("%Y")
        return weekday_and_month + day + year

    def get(self):
        """Return the middle section of the home page (index.html).

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
                    pretty_date=self._pretty_date(post["published"]),
                    description=post["description"],
                    read_more_link=read_more_link,
                )
        return home


class Archive(Page):
    """Define a class that gets the archive page's middle section."""

    # fmt: off
    _details_template = Template("""<details style="$style">
<summary>
$summary
</summary>
$contents
</details>\n""")
    # fmt: on

    def _link_to_post(self, post: dict) -> str:
        """Return a link with date and title to a post."""
        return self._link_template.substitute(
            href=post["file"], text=f"{post['published']}: {post['title']}"
        )

    def _browse_by_date(self, ascending: bool = True) -> str:
        """Return section that lets you browse by post date.

        If the caller specifies they want the dates in descending order,
        we iterate over the posts backwards.

        This method assumes the dates in the posts array are already
        sorted in ascending chronological order.
        """
        posts = self.info["posts"] if ascending else reversed(self.info["posts"])

        # TODO: Is this correct? PyCharm is telling me it thinks post
        # is a string, but it should be a dict.
        post_links = []
        for post in posts:
            post_links.append(self._link_to_post(post))
        browse_by_date = "<ul>\n"

        for post_link in post_links:
            browse_by_date += f"<li>{post_link}</li>\n"
        browse_by_date += "</ul>"

        return browse_by_date

    def _browse_by_tag(self) -> str:
        """Return section that lets you browse by tags.

        Each tag has its own details. You can link directly to the tag
        by using the href archive.html#[tag] where [tag] is the tag you
        want to link to.
        """
        posts = self.info["posts"]

        # Map each tag to a list of posts.
        tag_to_posts_map = {}
        for post in posts:
            for tag in post["tags"]:
                if tag in tag_to_posts_map:
                    tag_to_posts_map[tag].append(self._link_to_post(post))
                else:
                    tag_to_posts_map[tag] = [self._link_to_post(post)]

        # Create the browse by tag section.
        browse_by_tag = ""
        for tag in tag_to_posts_map:
            contents = f"<ul id={tag}>\n"
            for post_link in tag_to_posts_map[tag]:
                contents += f"<li>{post_link}</li>\n"
            contents += "</ul>"
            # This is nested, so we indent the details with inline
            # styling.
            tag_details = self._details_template.substitute(
                style="margin-left: 1em;", summary=f"{tag}", contents=contents
            )
            browse_by_tag += tag_details
        return browse_by_tag

    def get(self) -> str:
        """Return the middle section of the archive page."""
        browse_by_date_ascending = self._details_template.substitute(
            style="", summary="Browse by ascending date", contents=self._browse_by_date()
        )
        browse_by_date_descending = self._details_template.substitute(
            style="",
            summary="Browse by descending date",
            contents=self._browse_by_date(ascending=False),
        )
        browse_by_tag = self._details_template.substitute(
            style="", summary="Browse by tag", contents=self._browse_by_tag()
        )
        return browse_by_date_ascending + browse_by_date_descending + browse_by_tag
