"""Provide utilities to implement factory class."""
from typing import Callable
import inspect


class ArgumentInspector:
    """
    """

    def __init__(self, function: Callable, is_method: bool):
        """
        """
        self.function = function
        self.is_method = is_method

    def drop_invalid_arguments(self, arguments: dict) -> dict:
        """Remove the entries that cannot be passed to the function.

        Notes
        -----
        The functions with positional or var keyword parameters are
        not supported.

        Returns
        -------
        dict

        Return only the entries that the keys are
        members of the parameters.

        """

        if not self._is_supported():
            raise NotImplementedError(
                'The functions with var positional or '
                'var keyword parameters are not supported.')
        parameters = list(self._get_parameters().keys())
        valid_parameters = parameters[1:] if self.is_method else parameters
        return dict((parameter, argument)
                    for parameter, argument in arguments.items()
                    if parameter in valid_parameters)

    def _is_supported(self):
        if self._contains_kind(inspect.Parameter.VAR_KEYWORD):
            return False
        if self._contains_kind(inspect.Parameter.VAR_POSITIONAL):
            return False

        return True

    def _contains_kind(self, kind) -> bool:
        parameters = self._get_parameters()
        return len([name
                    for _, name
                    in parameters.items()
                    if name.kind == kind]) > 0

    def _get_parameters(self):
        signature = inspect.signature(self.function)
        return signature.parameters
