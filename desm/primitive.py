"""Implement a wrapper for primitive and strings."""
from dataclasses import dataclass
import abc


@dataclass
class Primitive(metaclass=abc.ABCMeta):
    """Wrapper for primitive and strings."""

    @abc.abstractproperty
    def primitive(self):
        """Return the raw value."""

    def handle(self, handler):
        """
        """
        return handler(self.primitive)
