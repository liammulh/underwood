"""Define our blog class that the user can call.

The generator requires a info file containing info on each page and post
in the blog. This info file is written in JSON.

This script also requires source files, written in HTML, for your blog.
These source files are meant to be sandwiched between HTML body tags.

Things that still need doing:
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

from src.underwood.feed import Feed
from src.underwood.file import File
from src.underwood.page import Archive
from src.underwood.page import Home
from src.underwood.page import Post
from src.underwood.section import Bottom
from src.underwood.section import Middle
from src.underwood.section import Top


class Blog:
    def __init__(self, path_to_info: str) -> None:
        """Initialize blog with provided path to info file."""
        self.info = File(path_to_info).read_json()

    def generate(self) -> None:
        """Generate the blog based on the provided info file."""

        pages = self.info["pages"]
        for page in pages:
            if ".html" in page["file"]:
                top = Top(self.info, page).contents()
                bottom = Bottom(self.info, page).contents()
                output_file = File(f"{self.info['output_dir']}/{page['file']}")
                if page["file"] == "index.html":
                    home = Home(self.info).contents()
                    output_file.write(top + home + bottom)
                elif page["file"] == "archive.html":
                    archive = Archive(self.info).contents()
                    output_file.write(top + archive + bottom)
                else:
                    middle = Middle(self.info, page).contents()
                    output_file.write(top + middle + bottom)
            elif page["file"] == "feed.xml":
                feed = Feed(self.info)
                feed.write()

        posts = self.info["posts"]
        for idx, post in enumerate(posts):
            if ".html" in post["file"]:
                output_file = File(f"{self.info['output_dir']}/{post['file']}")
                top = Top(self.info, post).contents()
                middle = Post(self.info, post).contents(idx)
                bottom = Bottom(self.info, post).contents()
                output_file.write(top + middle + bottom)
