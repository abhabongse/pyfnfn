# Author: Abhabongse Janthong <underneaththeunderneath@gmail.com>
# More info at https://github.com/abhabongse/python3-filewraps

import functools
import inspect
import io


class FileWrappedFunc(object):
    """
    A callable wrapper for a function which accepts filename as arguments in
    addition to file-like objects.
    """
    def __new__(cls, original_func, filearg=0, auto_close=True,
                open_kwargs=None):
        # Update attributes from original function.
        return functools.update_wrapper(super().__new__(cls), original_func)

    def __init__(self, original_func, filearg=0, auto_close=True,
                 open_kwargs=None):
        # Extract argument specs from original function.
        try:
            spec = inspect.getfullargspec(original_func)
            args = spec.args
            kwargs = spec.kwonlyargs
        except AttributeError:
            args = inspect.getargspec(original_func).args
            kwargs = []
        # Determine if a positional filearg is within bounds.
        try:
            filearg = args[filearg]
        except TypeError:
            pass  # recheck later whether it is a valid name
        except IndexError as e:
            e.args = ("argument list index out of range",)
            raise
        # Final check if filearg is valid.
        if filearg in args:
            pos = args.index(filearg)
        elif filearg in kwargs:
            pos = None
        else:
            raise NameError(
                "{name} is not a valid argument for the function {func}"
                .format(name=str(filearg), func=self._original_func.__name__)
                )

        # Keep track of necessary data.
        self.__signature__ = inspect.signature(original_func)
        self._original_func = original_func
        self._filearg = filearg
        self._pos = pos
        self._auto_close = auto_close
        self._open_kwargs = open_kwargs or {}


    def __call__(self, *args, **kwargs):
        """
        This method will be called when the wrapper function (which is this
        very object 'self') is invoked.
        """
        args = list(args)  # convert from non-mutable tuple to mutable list

        if self._pos is not None and self._pos < len(args):
            return self._wrapped_func(args, kwargs, args, self._pos,
                                      self._auto_close, self._open_kwargs)
        elif self._filearg in kwargs:
            return self._wrapped_func(args, kwargs, kwargs, self._filearg,
                                      self._auto_close, self._open_kwargs)
        else:
            return self._original_func(*args, **kwargs)

    def _wrapped_func(self, args, kwargs, store, key, auto_close, open_kwargs):
        """
        This method opens the file if necessary before the actual function is
        invoked. The file argument is identified by store[key] where store
        could be a list of positional arguments and key is an index, or the
        store could be a dictionary of keyword-only arguments and key is the
        name of the argument.
        """
        file = store[key]
        if isinstance(file, io.IOBase):
            return self._original_func(*args, **kwargs)
        elif auto_close:
            with open(file, **open_kwargs) as fileobj:
                store[key] = fileobj
                return self._original_func(*args, **kwargs)
        else:
            fileobj = open(file, **open_kwargs)
            store[key] = fileobj
            return self._original_func(*args, **kwargs)


def filewraps(original_func=None, filearg=0, auto_close=True, **open_kwargs):
    """
    A function wrapper that modifies the file argument to accept the filename
    string or the file descriptor integer in addition to file-like object.
    """
    if original_func is None:
        def decorator(original_func):
            return filewraps(original_func, filearg=filearg,
                             auto_close=auto_close, **open_kwargs)
        return decorator
    else:
        return FileWrappedFunc(original_func, filearg, auto_close, open_kwargs)
