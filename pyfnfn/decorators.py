# Author: Abhabongse Janthong
# More info at https://github.com/abhabongse/pyfnfn
"""Given a function which expects a file object as one of the input
arguments, the decorator in this module will modify the function input
entry point so that it additionally accepts file names without modifying
the implementation of the original function.
"""

__all__ = ('FunctionFilenameWrapper', 'fnfnwrap')

import functools
import inspect
import io

from .utils import is_valid_filename, check_open_kwargs

############################
##  Defining a decorator  ##
############################

def fnfnwrap(original_fn=None, *, filearg=0, **open_kwargs):
    """A function decorator that modifies a function definition to accept
    file name in additional to already-accepting file objects without
    actually modifying the implementation of the original function.

    Args:
        original_fn: Main function being wrapped
        filearg: Either the index of positional argument or the name of the
            argument itself, which accepts a file as input
        **open_kwargs: Arguments for built-in function `open()`. See the
            documentation for `open()` to see the list of input arguments.
    Returns:
        The same function with file open mechanics.
    """
    if original_fn is None:
        return functools.partial(fnfnwrap, filearg=filearg, **open_kwargs)
    else:
        return FunctionFilenameWrapper(original_fn, filearg, open_kwargs)

##############################
##  Wrapper implementation  ##
##############################

class FunctionFilenameWrapper(object):
    """A callable wrapper of a function accepting files as arguments.

    Given an original function `original_fn`, the name or the index of the
    file argument `filearg`, and a dictionary of keyword-only arguments
    `open_kwargs` to built-in function `open()`, this class wraps over the
    original function and will automatically open files when filename strings
    (provided as `str`, `bytes`, or `os.PathLike`) are given instead of file
    objects.

    Private Attributes (preceding with double underscores):
        original_fn: Main function being wrapped
        is_generator: Boolean whether `original_fn` is a generator function
        filearg: Name of function argument accepting files
        pos: Index of positional `filearg` argument, or None if keyword-only
        open_kwargs: Dictionary of keyword arguments to `open()`

    """

    def __new__(cls, original_fn, filearg=0, open_kwargs=None):
        # Update attributes from original function
        return functools.update_wrapper(super().__new__(cls), original_fn)

    def __init__(self, original_fn, filearg=0, open_kwargs=None):
        # Check if original function is callable
        if not callable(original_fn):
            raise TypeError('expected a callable function')
        # Check if open_kwargs is valid
        open_kwargs = open_kwargs or {}
        check_open_kwargs(open_kwargs)
        # Extract argument specs from original function
        spec = inspect.getfullargspec(original_fn)
        args = spec.args; kwargs = spec.kwonlyargs
        # Determine if positional filearg is within bounds
        try:
            filearg = args[filearg]  # obtain name of argument
        except TypeError:
            pass  # re-check later whether it is a valid name
        except IndexError as e:
            e.args = ("argument list index out of range",)
            raise
        # Check if filearg is actually valid
        if filearg in args:
            pos = args.index(filearg)
        elif filearg in kwargs:
            pos = None
        else:
            if isinstance(filearg, str):
                raise NameError(
                    "{name!r} is not a valid argument for the function {fn!r}"
                    .format(name=filearg, fn=original_fn.__qualname__)
                    )
            else:
                raise TypeError(
                    "{name!r} has incorrect type".format(name=filearg)
                    )
        # Keep track of data
        self.__original_fn = original_fn
        self.__is_generator =  inspect.isgeneratorfunction(original_fn)
        self.__filearg = filearg
        self.__pos = pos
        self.__open_kwargs = open_kwargs
        # Magic for compositable wrapper for multiple filename arguments
        self.__signature__ = inspect.signature(original_fn)

    def __call__(self, *args, **kwargs):
        """Invoke `original_fn` and open files as necessary.

        Args:
            args: List of given positional arguments
            kwargs: Dictionary of given keyword arguments
        Returns:
            Result from the invoked original function

        """
        args = list(args)  # convert from non-mutable tuple
        if self.__pos is not None and self.__pos < len(args):
            # Open files for positional argument
            return self.__invoke(args, kwargs, args, self.__pos)
        elif self.__filearg in kwargs:
            # Open files for keyword arguments
            return self.__invoke(args, kwargs, kwargs, self.__filearg)
        else:
            # Open files not necessary
            return self.__original_fn(*args, **kwargs)

    def __invoke(self, args, kwargs, store, key):
        """Open files given at `store[key]` before invoke actual function.

        Args:
            args: List of given positional arguments
            kwargs: Dictionary of given keyword arguments
            store: Either `args` or `kwargs` containing filename argument
            key: Lookup key for filename argument in `store`
        Returns:
            Result from the invoked original function

        """
        file_input = store[key]
        if isinstance(file_input, io.IOBase):
            # Input argument is already a file object
            return self.__original_fn(*args, **kwargs)
        elif is_valid_filename(file_input):
            # Input argument is a filename; need to open
            if self.__is_generator:
                # File needs to be opened inside a generator if the original
                # function is also a generator. A wrap is needed to maintain
                # the attributes information of the generator objects.
                @functools.wraps(self.__original_fn)
                def generator_wrapper():
                    with open(file_input, **self.__open_kwargs) as fileobj:
                        store[key] = fileobj
                        return (yield from self.__original_fn(*args, **kwargs))
                return generator_wrapper()
            else:
                # Open the file normally
                with open(file_input, **self.__open_kwargs) as fileobj:
                    store[key] = fileobj
                    return self.__original_fn(*args, **kwargs)
        else:
            raise TypeError(
                'unrecognized type for filename or file object for {filearg!r}'
                .format(filearg=self.__filearg)
                )

    def __get__(self, instance, owner):
        # In order to make this callable work with bounded methods inside
        # definition of classes, we make sure that this call is a non-data
        # descriptor. This part is heavily inspired by the documentation of
        # the package `wrapt` at
        # https://wrapt.readthedocs.io/en/latest/wrappers.html#function-wrappers
        get_method = self.__original_fn.__get__(instance, owner)
        return BoundFunctionFilenameWrapper(get_method)


class BoundFunctionFilenameWrapper(FunctionFilenameWrapper):
    """The bounded method version of the class FunctionFilenameWrapper"""
    def __get__(self, isinstance, owner):
        return self