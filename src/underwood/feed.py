"""Provides a class that is used to make an Atom feed."""

import xml.etree.ElementTree as et
from datetime import date

from src.underwood.file import File
from src.underwood.utils import uri, post_url


class Feed:
    """Define methods for making an Atom feed."""

    def __init__(self, info: dict) -> None:
        """Initialize the feed object with the blog info.

        Args:
            info: our JSON info containing metadata about our blog
        """
        self.info = info

        # Create the root element of the XML document so that our
        # methods have it.
        self.root = et.Element("feed", xmlns="http://www.w3.org/2005/Atom")

    def metadata(self) -> None:
        """Write metadata to the root element in the XML document."""
        et.SubElement(self.root, "title").text = self.info["domain_name"]
        # Borrow index.html's description for the subtitle. This assumes
        # index.html is the first page in the pages array. Not ideal,
        # but it's either this or duplicate the description in the JSON.
        # I'd rather the complexity reside in the code than in the JSON.
        # ¯\_(ツ)_/¯
        first_page = self.info["pages"][0]
        subtitle = (
            first_page["description"]
            if first_page["file"] == "index.html"
            else "Insert subtitle here"
        )
        et.SubElement(self.root, "subtitle").text = subtitle
        et.SubElement(
            self.root, "id"
        ).text = f"tag:{self.info['domain_name']},{self.info['inception_date']}:/"
        et.SubElement(self.root, "updated").text = date.today().strftime("%Y-%m-%d")
        et.SubElement(
            self.root,
            "link",
            rel="alternate",
            type="text/html",
            href=f"https://{self.info['domain_name']}/",
        )

    def entry(self, post: dict) -> None:
        """Write a single entry to the root element of the XML document.

        Args:
            post: blog post we're making an entry for
        """
        entry = et.SubElement(self.root, "entry")

        # Write author element to the entry.
        author = et.SubElement(entry, "author")
        et.SubElement(author, "name").text = self.info["author"]
        site_url = post_url(self.info["domain_name"], "")
        et.SubElement(author, "uri").text = site_url

        # Write post-specific elements to the entry.
        et.SubElement(entry, "title").text = post["description"]
        url = post_url(self.info["domain_name"], post["file"])
        et.SubElement(entry, "link").text = url
        et.SubElement(entry, "id").text = uri(self.info, post)
        if "updated" in post:
            updated = post["updated"]
        else:
            updated = post["published"]
        et.SubElement(entry, "updated").text = updated
        et.SubElement(entry, "published").text = post["published"]
        for tag in post["tags"]:
            et.SubElement(entry, "category", scheme=url, term=tag)
        et.SubElement(entry, "summary", type="html").text = post["description"]

    def entries(self):
        """Write all entries to the root of the XML document."""
        for post in self.info["posts"]:
            self.entry(post)

    def write(self):
        """Write the Atom feed to disk."""
        self.metadata()
        self.entries()
        xml_declaration = '<?xml version="1.0" encoding="utf-8"?>\n'
        output_file = File(f"{self.info['output_dir']}/feed.xml")
        et.indent(self.root)
        output_file.write(xml_declaration + et.tostring(self.root, encoding="unicode"))