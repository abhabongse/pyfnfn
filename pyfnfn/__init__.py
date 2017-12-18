# Author: Abhabongse Janthong <underneaththeunderneath@gmail.com>
# More info at https://github.com/abhabongse/pyfnfn
"""Given a function which expects a file object as one of the input
arguments, the decorator in this module will modify the function input
entry point so that it additionally accepts file names without modifying
the implementation of the original function.
"""
# This docstring is copied from decorators.py

__all__ = ('FunctionFilenameWrapper', 'fnfnwrap')

from .decorators import FunctionFilenameWrapper, fnfnwrap
