"""Defines utility functions.

Ideas for improvement:
    - Move these into modules where they are used?
"""

from datetime import datetime as dt


def uri(info, page):
    """Returns an RFC 4151 tag URI given the info and page or post.

    For more information on RFC 4151, see the link below:
    https://datatracker.ietf.org/doc/html/rfc4151

    Args:
        info: our JSON info containing metadata about our blog
        page: (or post) we want a URI for
    Returns:
        a URI of the form tag:foobar.org,yyyy-mm-dd:/path/to/file.html
    """
    domain = info["domain_name"]
    pubdate = page["published"]
    return f"tag:{domain},{pubdate}:/{page['file']}"


def pretty_date(iso_8601_date: str) -> str:
    """Returns a date whose format is: Thursday, January 1, 1970.

    Args:
        iso_8601_date: date with format yyyy-mm-dd
    """
    date_obj = dt.strptime(iso_8601_date, "%Y-%m-%d")
    weekday_and_month = date_obj.strftime("%A, %B ")
    day = date_obj.strftime("%d").lstrip("0") + ", "
    year = date_obj.strftime("%Y")
    return weekday_and_month + day + year


def post_url(domain_name: str, file: str) -> str:
    """Returns a post's URL given its domain name and file.

    Args:
         domain_name: domain name listed in the blog info
         file: file associated with the blog post
    """
    return f"https://www.{domain_name}/{file}"
