"""Implement a class that represents document."""
from typing import List
from dataclasses import dataclass


@dataclass
class Document:
    """Represent a tokenized document."""

    tokens: List[str]
