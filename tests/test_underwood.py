"""Use underwood to generate a test blog."""

from src.underwood.blog import Blog


def test_underwood():
    """Barf out a blog that we have to manually check for issues."""
    test_blog = Blog("tests/data/test.json")
    test_blog.generate()
