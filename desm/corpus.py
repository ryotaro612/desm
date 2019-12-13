"""Provide a class that represent a corpus."""
import contextlib
from typing import Iterator
from .text import Text


class Corpus:
    """A corpus to train a word2vec model."""

    def __init__(self, filename: str):
        """Take a path to a corpus file."""
        self.filename = filename

    @contextlib.contextmanager
    def __call__(self) -> Iterator[Text]:
        """Create an iterator that emits a text at a time."""
        with open(self.filename) as stream:
            yield (Text(line.strip()) for line in stream)

    @classmethod
    def create_from_file(cls, filename: str):
        """Create a :py:class:`Corpus` from a file.

        Returns
        -------
        Corpus

        """
        return Corpus(filename)
