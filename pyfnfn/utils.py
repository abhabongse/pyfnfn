# Author: Abhabongse Janthong
# More info at https://github.com/abhabongse/pyfnfn
"""Helper functions."""

__all__ = ('is_valid_filename', 'validate_open_kwargs')

import inspect
import os


def is_valid_filename(filename):
    """Check if the content of `filename` is of a valid string type:
    `str`, `bytes`, or `os.PathLike`.

    Args:
        filename: An object representing a file name
    Returns:
        A boolean indicating whether it is a valid type for file name
    """
    try:
        return isinstance(filename, str) \
            or isinstance(filename, bytes) \
            or isinstance(filename, os.PathLike)
    except AttributeError:  # os.PathLike skipped if not exists
        return False


def validate_open_kwargs(kwargs):
    """Check if keywork arguments dictionary are suitable for built-in
    `open()` function.

    Args:
        kwargs: A dictionary of potential keyword arguments for `open()`
    Returns:
        None if all keyword argument names are valid
    Raises:
        TypeError if some keywords are not valid
    """
    open_spec = list(inspect.signature(open).parameters)[1:]
    for kwarg in kwargs:
        if kwarg not in open_spec:
            raise TypeError(
                '{kwarg!r} is not a valid argument for built-in function open'
                .format(kwarg=kwarg)
                )
