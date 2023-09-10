"""Provides a class that returns sections of our HTML document.

This class handles the logic of creating each section of the HTML
document, e.g. the top of the document. There is another class that we
use in this class that defines templates for the HTML document.

Ideas for improvement:
    - Rename modules to conform to PEP8.
    - https://peps.python.org/pep-0008/#package-and-module-names
    - Rename this module section? Rename class HTMLSection?
    - Move the templates from HTMLTemplate into this module.
    - Divide the sections into their own classes that inherit from the
      base class? For example: Top, Middle, Archive, Bottom, etc.
    - The Top class would include the top template, for example.
"""

from balblog.Config import Config
from balblog.File import File
from balblog.HTMLTemplate import HTMLTemplate
from balblog.utils import pretty_date


class HTMLDocument:
    """Defines methods that return sections of our HTML document."""

    def __init__(self, info: dict, page: dict) -> None:
        """Initializes the HTML document object.

        Args:
            info: our JSON info containing metadata about our blog
            page: (or post) containing info about the page we are making
        """
        self.info = info
        self.page = page  # This can be used for pages or posts.

    def nav_links(self) -> str:
        """Returns a set of links for each page specified in blog info.

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

    def top(self) -> str:
        """Returns the top of the HTML document.

        This is the head tag along with its contents, the opening body
        tag, and whatever else we want at the top of each page or post.
        """
        return HTMLTemplate.top.substitute(
            domain_name=self.info["domain_name"],
            title=self.page["title"],
            description=self.page["description"],
            nav_links=self.nav_links(),
        )

    def middle(self) -> str:
        """Returns the content of the HTML document.

        This is the stuff we want to sandwich between the body tags.
        """
        path = f"{self.info['input_dir']}/{self.page['file']}"
        file = File(path)
        return file.read()

    @staticmethod
    def link_to_post(post: dict) -> str:
        """Returns a link with date and title to a post."""
        return HTMLTemplate.link.substitute(
            href=post["file"], text=f"{post['published']}: {post['title']}"
        )

    def browse_by_date(self, ascending: bool = True) -> str:
        """Returns section that lets you browse by post date.

        If the caller specifies they want the dates in descending order,
        we iterate over the posts backwards.

        This method assumes the dates in the posts array are already
        sorted in ascending chronological order.
        """
        posts = self.info["posts"] if ascending else reversed(self.info["posts"])

        post_links = []
        for post in posts:
            post_links.append(
                HTMLTemplate.link.substitute(
                    href=post["file"], text=f"{self.link_to_post(post)}"
                )
            )

        browse_by_date = "<ul>\n"
        for post_link in post_links:
            browse_by_date += f"<li>{post_link}</li>\n"
        browse_by_date += "</ul>"
        return browse_by_date

    def browse_by_tag(self) -> str:
        """Returns section that lets you browse by tags.

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
                    tag_to_posts_map[tag].append(self.link_to_post(post))
                else:
                    tag_to_posts_map[tag] = [self.link_to_post(post)]

        # Create the browse by tag section.
        browse_by_tag = ""
        for tag in tag_to_posts_map:
            contents = f"<ul id={tag}>\n"
            for post_link in tag_to_posts_map[tag]:
                contents += f"<li>{post_link}</li>\n"
            contents += "</ul>"
            # This is nested, so we indent the details with inline
            # styling.
            tag_details = HTMLTemplate.details.substitute(
                style="margin-left: 1em;", summary=f"{tag}", contents=contents
            )
            browse_by_tag += tag_details
        return browse_by_tag

    def archive(self) -> str:
        """Returns the contents of the archive page."""
        browse_by_date_ascending = HTMLTemplate.details.substitute(
            style="", summary="Browse by ascending date", contents=self.browse_by_date()
        )
        browse_by_date_descending = HTMLTemplate.details.substitute(
            style="",
            summary="Browse by descending date",
            contents=self.browse_by_date(ascending=False),
        )
        browse_by_tag = HTMLTemplate.details.substitute(
            style="", summary="Browse by tag", contents=self.browse_by_tag()
        )
        return browse_by_date_ascending + browse_by_date_descending + browse_by_tag

    def home(self) -> str:
        """Returns the contents of the home page (index.html).

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
                post_title_link = HTMLTemplate.link.substitute(
                    href=post["file"], text=post["title"]
                )
                read_more_link = HTMLTemplate.link.substitute(
                    href=post["file"], text="Read more..."
                )
                home += HTMLTemplate.post_summary.substitute(
                    post_title_link=post_title_link,
                    pretty_date=pretty_date(post["published"]),
                    description=post["description"],
                    read_more_link=read_more_link,
                )
        return home

    @staticmethod
    def post_info(post: dict) -> str:
        """Returns info about the post including dates and tags.

        We want the user to know when the post was published and
        if/when updated.

        We also want the user to know what the post is tagged under, and
        we want to provide links to the comprehensive list of posts for
        the tags.
        """

        date_info = ""
        date_info += f"<div>Published: {pretty_date(post['published'])}</div>\n"
        if "updated" in post:
            date_info += f"<div>Updated: {pretty_date(post['updated'])}</div>\n"

        tag_info = ""
        tags = post["tags"]
        if len(tags) > 0:
            tag_info += "<div>Tagged under: "
        for idx, tag in enumerate(tags):
            tag_info += HTMLTemplate.link.substitute(
                href=f"archive.html#{tag}", text=tag
            )
            at_end = idx + 1 == len(tags)
            if at_end:
                tag_info += "</div>\n"
            else:
                tag_info += ", "

        post_info = date_info + tag_info + "<hr/>\n"
        return post_info

    def prev_next_links(self, post_idx: int) -> str:
        """Returns the previous and/or next links.

        We provide links to the previous and next posts if the post has
        both. If the post only has a previous post or only has a next
        post, we provide the link to the previous or next post.
        """
        posts = self.info["posts"]
        prev_andor_next = ""
        if len(posts) > 1:
            at_beginning = post_idx == 0
            in_middle = 0 < post_idx < len(posts) - 1
            at_end = post_idx == len(posts) - 1
            can_define_prev = post_idx - 1 >= 0
            if can_define_prev:
                prev_link = HTMLTemplate.link.substitute(
                    href=posts[post_idx - 1]["file"], text="Previous post"
                )
            can_define_next = post_idx + 1 <= len(posts) - 1
            if can_define_next:
                next_link = HTMLTemplate.link.substitute(
                    href=posts[post_idx + 1]["file"], text="Next post"
                )
            if at_beginning:
                prev_andor_next = next_link
            elif in_middle:
                prev_andor_next = prev_link + " | " + next_link
            elif at_end:
                prev_andor_next = prev_link
        return prev_andor_next

    @staticmethod
    def bottom() -> str:
        """Returns the bottom of the HTML document."""
        return HTMLTemplate.bottom
