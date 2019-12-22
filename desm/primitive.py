from dataclasses import dataclass
import abc

@dataclass
class Primitive(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def primitive(self):
        """
        """

    def handle(self, handler):
        """
        """
        return handler(self.primitive)
