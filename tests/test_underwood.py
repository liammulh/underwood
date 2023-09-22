"""Use underwood to generate a test blog."""

from src.underwood.blog import Blog


def test_underwood() -> None:
    """Barf out a blog that we have to manually check for issues.

    Before we generate the blog, we validate its JSON info file.
    """
    test_blog = Blog("tests/data/test.json")
    test_blog.validate()
    test_blog.generate()
