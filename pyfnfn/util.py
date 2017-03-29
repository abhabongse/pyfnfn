# Author: Abhabongse Janthong <underneaththeunderneath@gmail.com>
# More info at https://github.com/abhabongse/pyfnfn
"""Modify a function to accept filenames in addition to file objects without
modifying the implementation of the function.

"""
__all__ = ('is_valid_filename', 'check_open_kwargs')

import inspect
import os


def is_valid_filename(filename):
    """Check if filename is of a valid type (`str`, `bytes`, or `os.PathLike`).

    Args:
        filename: An object representing a filename
    Returns:
        A boolean indicating whether it is a valid type for filename.

    """
    try:
        return isinstance(filename, str) \
            or isinstance(filename, bytes) \
            or isinstance(filename, os.PathLike)
    except AttributeError:
        return False


def check_open_kwargs(kwargs):
    """Makes sure that keyword arguments are suitable for built-in `open()`.

    Args:
        kwargs: Dictionary of potential keyword arguments for `open()`
    Returns:
        None if all keyword argument names are valid
    Raises:
        TypeError if some keyword argument names are not valid

    """
    open_arguments = inspect.getfullargspec(open).args[1:]
    for kwarg in kwargs:
        if kwarg not in open_arguments:
            raise TypeError(
                '{kwarg!r} is not a valid argument for built-in function open'
                .format(kwarg=kwarg)
                )
