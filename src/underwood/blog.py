"""Provide our blog class that the user can call."""

from jsonschema import validate as validate_json

from src.underwood.feed import Feed
from src.underwood.file import File
from src.underwood.page import Archive
from src.underwood.page import Home
from src.underwood.page import Post
from src.underwood.schema import schema
from src.underwood.section import Bottom
from src.underwood.section import Middle
from src.underwood.section import Top
from src.underwood.keys import Keys


class Blog:
    """Define the blog class.

    This is user-facing. A user will import this class and use it to
    create their blog object.
    """

    def __init__(self, path_to_info: str) -> None:
        """Initialize blog with provided path to info file."""
        self.info = File(path_to_info).read_json()

    def validate(self) -> None:
        """Validate the provided info file."""
        validate_json(self.info, schema)

    def generate(self) -> None:
        """Generate the blog based on the provided info file."""

        pages = self.info[Keys.PAGES.value]
        for page in pages:
            if ".html" in page[Keys.FILE_NAME.value]:
                top = Top(self.info, page).contents()
                bottom = Bottom(self.info, page).contents()
                output_file = File(
                    f"{self.info[Keys.OUTPUT_DIR_PATH.value]}/{page[Keys.FILE_NAME.value]}"
                )
                if page[Keys.FILE_NAME.value] == "index.html":
                    home = Home(self.info).contents()
                    output_file.write(top + home + bottom)
                elif page[Keys.FILE_NAME.value] == "archive.html":
                    archive = Archive(self.info).contents()
                    output_file.write(top + archive + bottom)
                else:
                    middle = Middle(self.info, page).contents()
                    output_file.write(top + middle + bottom)
            elif page[Keys.FILE_NAME.value] == "feed.xml":
                feed = Feed(self.info)
                feed.write()

        posts = self.info[Keys.POSTS.value]
        for idx, post in enumerate(posts):
            if ".html" in post[Keys.FILE_NAME.value]:
                output_file = File(
                    f"{self.info[Keys.OUTPUT_DIR_PATH.value]}/{post[Keys.FILE_NAME.value]}"
                )
                top = Top(self.info, post).contents()
                middle = Post(self.info, post).contents(idx)
                bottom = Bottom(self.info, post).contents()
                output_file.write(top + middle + bottom)
