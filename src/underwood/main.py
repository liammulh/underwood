"""Given JSON info file and source files, generates a static blog.

This script requires a JSON info file. See the JSON info file for an
example.

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
    - Create a blog class where you can initialize a blog with an info
    JSON file.
        - The blog class should have a generate method that does what
        the main function does right now.
    - Allow user to specify stylesheets and scripts in info JSON file.
"""

from src.underwood.Config import Config
from src.underwood.Feed import Feed
from src.underwood.File import File
from src.underwood.HTMLDocument import HTMLDocument


info = File(Config.INFO.value).read_json()


def main():
    pages = info["pages"]
    for page in pages:
        if ".html" in page["file"]:
            doc = HTMLDocument(info, page)
            output_file = File(f"{info['output_dir']}/{page['file']}")
            if page["file"] == "index.html":
                output_file.write(doc.top() + doc.home() + doc.bottom())
            elif page["file"] == "archive.html":
                output_file.write(doc.top() + doc.archive() + doc.bottom())
            else:
                output_file.write(doc.top() + doc.middle() + doc.bottom())
        elif page["file"] == "feed.xml":
            feed = Feed(info)
            feed.write()

    posts = info["posts"]
    for idx, post in enumerate(posts):
        if ".html" in post["file"]:
            doc = HTMLDocument(info, post)
            output_file = File(f"{info['output_dir']}/{post['file']}")
            post_middle = doc.post_info(post) + doc.middle() + doc.prev_next_links(idx)
            output_file.write(doc.top() + post_middle + doc.bottom())


if __name__ == "__main__":
    main()
