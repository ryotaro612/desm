"""
"""
import dataclasses as d
import contextlib


@d.dataclass
class ModelLocation:
    """Location of a model."""

    location: str

    @classmethod
    def create(cls, path: str):
        """Create :py:class:`ModelLocation` from a local path."""
        return ModelLocation(path)

    @contextlib.contextmanager
    def open_writable_stream(self):
        """
        """
        with open(self.location, 'wb') as file_object:
            yield file_object
