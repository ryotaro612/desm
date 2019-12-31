"""Provide classes that represent first class collections."""
import abc
import contextlib


class FirstClassFileContextManagerProvider(metaclass=abc.ABCMeta):
    """Provide a context manager."""

    def __init__(self, filename: str):
        """
        """
        self.filename = filename

    @contextlib.contextmanager
    def __call__(self):
        """
        """
        with open(self.filename) as stream:
            yield (self.transform(item.strip()) for item in stream)

    @abc.abstractmethod
    def transform(self, item):
        """
        """


class FirstClassSequence(metaclass=abc.ABCMeta):
    """
    """

    @abc.abstractproperty
    def sequence(self):
        """
        """

    def __getitem__(self, s):
        """
        """
        return self.sequence.__getitem__(s)

    def __len__(self):
        return len(self.sequence)
