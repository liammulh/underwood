"""Define the JSON schema our info file needs to conform to.

For more info on JSON schemas, see:
https://json-schema.org/

For more info on the specific Python package we use to validate our info
file, see:
https://python-jsonschema.readthedocs.io/
"""

# We don't care about long lines for this file.
# pylint: disable=C0301

from underwood.keys import Keys

schema = {
    "type": "object",
    "description": "This is the info we need to generate our blog.",
    "properties": {
        Keys.DOMAIN_NAME.value: {
            "type": "string",
            "description": "This is the domain name of the blog, e.g. foobar.org.",
        },
        Keys.DATE_STARTED.value: {
            "type": "string",
            "description": "This is the date we started our blog. It is used in the Atom feed.",
        },
        Keys.PRIMARY_AUTHOR.value: {
            "type": "string",
            "description": "This is the primary author of the blog.",
        },
        Keys.INPUT_DIR_PATH.value: {
            "type": "string",
            "description": "This is the path to the directory containing source HTML for the blog.",
        },
        Keys.OUTPUT_DIR_PATH.value: {
            "type": "string",
            "description": "This is the path to the directory where the generated blog is outputted.",
        },
        Keys.PAGES.value: {
            "type": "array",
            "description": "An array of pages in the blog.",
            "items": {
                "type": "object",
                "properties": {
                    Keys.FILE_NAME.value: {
                        "type": "string",
                        "description": "This is the name of the file for the page, e.g. about.html.",
                    },
                    Keys.TITLE.value: {
                        "type": "string",
                        "description": "This is the title of the page.",
                    },
                    Keys.DESCRIPTION.value: {
                        "type": "string",
                        "description": "This is a short description of the page.",
                    },
                },
                "required": [
                    Keys.FILE_NAME.value,
                    Keys.TITLE.value,
                    Keys.DESCRIPTION.value,
                ],
            },
        },
        Keys.POSTS.value: {
            "type": "array",
            "description": "An array of blog posts.",
            "items": {
                "type": "object",
                "properties": {
                    Keys.FILE_NAME.value: {
                        "type": "string",
                        "description": "This is the name of the file for the post, e.g. foo-post.html.",
                    },
                    Keys.TITLE.value: {
                        "type": "string",
                        "description": "This is a short title for the post.",
                    },
                    Keys.POST_TITLE.value: {
                        "type": "string",
                        "description": "This is a more descriptive title for the post.",
                    },
                    Keys.DESCRIPTION.value: {
                        "type": "string",
                        "description": "This is a short description of the post.",
                    },
                    Keys.TAGS.value: {
                        "type": "array",
                        "description": "An array of tags for the post.",
                        "items": {
                            "type": "string",
                            "description": "A tag in lowercase-kebab-case.",
                        },
                    },
                    Keys.DATE_PUBLISHED.value: {
                        "type": "string",
                        "description": "ISO 8601 date when the post was first published.",
                    },
                    Keys.DATE_UPDATED.value: {
                        "type": "string",
                        "description": "ISO 8601 date when the post was last updated.",
                    },
                },
                "required": [
                    Keys.FILE_NAME.value,
                    Keys.TITLE.value,
                    Keys.POST_TITLE.value,
                    Keys.DESCRIPTION.value,
                    Keys.TAGS.value,
                    Keys.DATE_PUBLISHED.value,
                ],
            },
        },
    },
    "required": [
        Keys.DOMAIN_NAME.value,
        Keys.DATE_STARTED.value,
        Keys.PRIMARY_AUTHOR.value,
        Keys.INPUT_DIR_PATH.value,
        Keys.OUTPUT_DIR_PATH.value,
        Keys.PAGES.value,
        Keys.POSTS.value,
    ],
}
