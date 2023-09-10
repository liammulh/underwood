"""Define our blog class that the user can call.

The generator requires a info file containing info on each page and post
in the blog. This info file is written in JSON.

This script also requires source files, written in HTML, for your blog.
These source files are meant to be sandwiched between HTML body tags.

Things that still need doing:
    - Use imperative mood in docstrings.
    - Create JSON schema and validate blog.json.
    - Use enum for info keys, so they can be easily renamed.
    - Consider improvements written in each module.
    - Add tests.
    - Add docs on blog.json to README.
        - Mention that you can add an updated field to each post.
    - Edit inception date in blog.json.
    - Allow user to specify stylesheets and scripts in info JSON file.
    - If a method should be private, prepend the method name with an
    underscore.
"""

from src.underwood.Feed import Feed
from src.underwood.File import File
from src.underwood.HTMLDocument import HTMLDocument


class Blog:
    def __init__(self, path_to_info: str) -> None:
        """Initialize blog with provided path to info file."""
        self.info = File(path_to_info).read_json()

    def generate(self):
        """Generate the blog based on the provided info file."""
        pages = self.info["pages"]
        for page in pages:
            if ".html" in page["file"]:
                doc = HTMLDocument(self.info, page)
                output_file = File(
                    f"{self.info['output_dir']}/{page['file']}")
                if page["file"] == "index.html":
                    output_file.write(
                        doc.top() + doc.home() + doc.bottom())
                elif page["file"] == "archive.html":
                    output_file.write(
                        doc.top() + doc.archive() + doc.bottom())
                else:
                    output_file.write(
                        doc.top() + doc.middle() + doc.bottom())
            elif page["file"] == "feed.xml":
                feed = Feed(self.info)
                feed.write()

        posts = self.info["posts"]
        for idx, post in enumerate(posts):
            if ".html" in post["file"]:
                doc = HTMLDocument(self.info, post)
                output_file = File(
                    f"{self.info['output_dir']}/{post['file']}")
                post_middle = doc.post_info(
                    post) + doc.middle() + doc.prev_next_links(idx)
                output_file.write(
                    doc.top() + post_middle + doc.bottom())
