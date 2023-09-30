"""Provide a class that is used to make an Atom feed."""

import xml.etree.ElementTree as ET
from datetime import date

from underwood.file import File


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
        self.root = ET.Element("feed", xmlns="http://www.w3.org/2005/Atom")

    @staticmethod
    def _post_url(domain_name: str, file: str) -> str:
        """Return a post's URL given its domain name and file.

        Args:
             domain_name: domain name listed in the blog info
             file: file associated with the blog post
        """
        return f"https://www.{domain_name}/{file}"

    def _uri(self, page: dict) -> str:
        """Return an RFC 4151 tag URI given the info and page or post.

        For more information on RFC 4151, see the link below:
        https://datatracker.ietf.org/doc/html/rfc4151

        Args:
            page: (or post) we want a URI for
        Returns:
            a URI of the form tag:foobar.org,yyyy-mm-dd:/path/to/file.html
        """
        domain = self.info["domain_name"]
        pubdate = page["published"]
        return f"tag:{domain},{pubdate}:/{page['file']}"

    def _add_metadata(self) -> None:
        """Add metadata to the root element in the XML document."""
        ET.SubElement(self.root, "title").text = self.info["domain_name"]
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
        ET.SubElement(self.root, "subtitle").text = subtitle
        ET.SubElement(
            self.root, "id"
        ).text = f"tag:{self.info['domain_name']},{self.info['inception_date']}:/"
        ET.SubElement(self.root, "updated").text = date.today().strftime("%Y-%m-%d")
        ET.SubElement(
            self.root,
            "link",
            rel="alternate",
            type="text/html",
            href=f"https://{self.info['domain_name']}/",
        )

    def _add_entry(self, post: dict) -> None:
        """Add a single entry to the root element of the XML document.

        Args:
            post: blog post we're making an entry for
        """
        entry = ET.SubElement(self.root, "entry")

        # Write author element to the entry.
        author = ET.SubElement(entry, "author")
        ET.SubElement(author, "name").text = self.info["author"]
        site_url = self._post_url(self.info["domain_name"], "")
        ET.SubElement(author, "uri").text = site_url

        # Write post-specific elements to the entry.
        ET.SubElement(entry, "title").text = post["description"]
        url = self._post_url(self.info["domain_name"], post["file"])
        ET.SubElement(entry, "link").text = url
        ET.SubElement(entry, "id").text = self._uri(post)
        if "updated" in post:
            updated = post["updated"]
        else:
            updated = post["published"]
        ET.SubElement(entry, "updated").text = updated
        ET.SubElement(entry, "published").text = post["published"]
        for tag in post["tags"]:
            ET.SubElement(entry, "category", scheme=url, term=tag)
        ET.SubElement(entry, "summary", type="html").text = post["description"]

    def _add_entries(self) -> None:
        """Add all entries to the root of the XML document."""
        for post in self.info["posts"]:
            self._add_entry(post)

    def write(self) -> None:
        """Write the Atom feed to disk."""
        self._add_metadata()
        self._add_entries()
        xml_declaration = '<?xml version="1.0" encoding="utf-8"?>\n'
        output_file = File(f"{self.info['output_dir']}/feed.xml")
        ET.indent(self.root)
        output_file.write(xml_declaration + ET.tostring(self.root, encoding="unicode"))
