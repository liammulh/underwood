"""Provide an enum with the keys for our info object.

Throughout the code base, we refer to the JSON file that contains our
blog's information (domain name, author, input directory, output
directory, etc.) as the info file. This module defines an enum that
contains each key in the info file.
"""

from enum import Enum


class Keys(Enum):
    """Enumerate the keys of our info object.

    This allows us to rename the keys without needing to worry about
    missing a rename. For a description of each key, see the schema.
    """

    DATE_PUBLISHED = "published"
    DATE_STARTED = "inception_date"
    DATE_UPDATED = "updated"
    DESCRIPTION = "description"
    DOMAIN_NAME = "domain_name"
    FILE_NAME = "file"
    INPUT_DIR_PATH = "input_dir"
    OUTPUT_DIR_PATH = "output_dir"
    PAGES = "pages"
    POSTS = "posts"
    POST_TITLE = "post_title"
    PRIMARY_AUTHOR = "author"
    TAGS = "tags"
    TITLE = "title"
