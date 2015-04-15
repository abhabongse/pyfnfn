#!/usr/bin/env python3
#
# Author: Abhabongse Janthong <underneaththeunderneath@gmail.com>
# More info at https://github.com/abhabongse/python3-filewraps
#


class FileWrappedFunction(object):
    """
    A callable wrapper for a function that should accept filename as arguments
    in addition to file-like objects.
    """
    def __init__(self, original_func, filearg=0, auto_close=True, open_kwargs=None):

        import inspect

        self._original_func = original_func
        self._sig = inspect.signature(original_func)
        self._spec = inspect.getfullargspec(original_func)
        self._auto_close = auto_close
        self._open_kwargs = open_kwargs or {}

        # Convert the variable name to string if integer is given.
        try:
            self._filearg = self._spec.args[filearg]
        except TypeError:
            self._filearg = filearg
        except IndexError as e:
            e.args = ("argument list index out of range",)
            raise e

        # CASE 1: the given variable is positional.
        if self._filearg in self._spec.args:
            self._pos = self._spec.args.index(self._filearg)

        # CASE 2: the given variable is keyword-only.
        elif self._filearg in self._spec.kwonlyargs:
            pass  # do nothing

        # OTHERWISE: the given variable does not exist.
        else:
            raise NameError("{name} is not a valid argument for the function {func}"
                            .format(name=str(self._filearg), func=original_func.__name__))

    def __call__(self, *args, **kwargs):
        ba = self._sig.bind(*args, **kwargs)
        args, kwargs = list(ba.args), ba.kwargs

        if hasattr(self, '_pos') and self._pos < len(args):
            return self._wrapped_func(args, kwargs, args, self._pos)
        elif self._filearg in kwargs:
            return self._wrapped_func(args, kwargs, kwargs, self._filearg)
        else:
            return self._original_func(*args, **kwargs)

    def _wrapped_func(self, args, kwargs, store, key):
        """
        Called by _func_by_position or _func_by_keyword if the file argument
        is given and file may need to be opened.
        """
        import io

        file = store[key]
        if isinstance(file, io.IOBase):
            return self._original_func(*args, **kwargs)
        elif self._auto_close:
            with open(file, **self._open_kwargs) as fileobj:
                store[key] = fileobj
                return self._original_func(*args, **kwargs)
        else:
            fileobj = open(file, **self._open_kwargs)
            store[key] = fileobj
            return self._original_func(*args, **kwargs)


def filewraps(original_func=None, *, filearg=0, auto_close=True, **open_kwargs):
    """
    Function wrapper that modifies the file argument to accept the filename
    string or the file descriptor integer in addition to file-like object.
    """
    import functools

    if original_func is None:
        def decorator(original_func):
            return filewraps(original_func, filearg=filearg, auto_close=auto_close,
                             **open_kwargs)
        return decorator
    elif not hasattr(original_func, '_original_func'):
        func = FileWrappedFunction(original_func, filearg, auto_close, open_kwargs)
        func = functools.update_wrapper(func, original_func)
        return func
    else:
        raise NotImplementedError("Composable @filewraps decorator not yet implemented.")
