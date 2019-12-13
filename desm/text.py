"""Expose :py:class:`Text` that represents a text."""
from dataclasses import dataclass


@dataclass
class Text:
    """Reprensent a text."""

    text: str
