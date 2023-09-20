"""Provide a class that has helper methods for dealing with files."""

import json


class File:
    """Define helper methods for dealing with files."""

    def __init__(self, path: str) -> None:
        """Initialize the file object.

        Args:
             path: either relative to the current directory or absolute
        """
        self.path = path

    def read(self) -> str:
        """Return the contents of a file."""
        with open(self.path, encoding="utf-8") as file:
            return file.read()

    def read_json(self) -> dict:
        """Return the contents of a JSON file."""
        return json.loads(self.read())

    def write(self, string: str) -> None:
        """Write contents to a file.

        If the file doesn't exist, create it. If it does exist,
        overwrite the existing contents.
        """
        with open(self.path, mode="w+", encoding="utf-8") as file:
            file.write(string)
