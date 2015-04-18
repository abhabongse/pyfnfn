#
# Author: Abhabongse Janthong <underneaththeunderneath@gmail.com>
# More info at https://github.com/abhabongse/python3-filewraps
#


class FileWrappedFunction(object):
    """
    A callable wrapper for a function that should accept filename as arguments
    in addition to file-like objects.
    """
    def __init__(self, original_func):
        import inspect
        self._original_func = original_func
        self._spec = inspect.getfullargspec(original_func)
        self._fileargs = []  # list of (name, auto_close, open_kwargs)

    def add_filearg(self, filearg=0, auto_close=True, open_kwargs=None):
        """
        Append a new file argument to the callable class object.
        This function is called once per one file argument binding.
        """
        try:
            filearg = self._spec.args[filearg]
        except TypeError:
            pass
        except IndexError as e:
            e.args = ("argument list index out of range",)
            raise e

        # CASE 1: the given variable is positional.
        if filearg in self._spec.args:
            pos = self._spec.args.index(filearg)

        # CASE 2: the given variable is keyword-only.
        elif filearg in self._spec.kwonlyargs:
            pos = None

        # OTHERWISE: the given variable does not exist.
        else:
            raise NameError("{name} is not a valid argument for the function {func}"
                            .format(name=str(self._filearg), func=original_func.__name__))

        self._fileargs.append((filearg, pos, auto_close, open_kwargs or {}))

    def __call__(self, *args, **kwargs):
        """
        This method will be called when the class object is called as callable.
        """
        args = list(args)  # convert from (non-mutable) tuple to (mutable) list
        filearg, pos, auto_close, open_kwargs = self._fileargs[0]

        if pos is not None and pos < len(args):
            return self._wrapped_func(args, kwargs, args, pos, auto_close, open_kwargs)
        elif filearg in kwargs:
            return self._wrapped_func(args, kwargs, kwargs, filearg, auto_close, open_kwargs)
        else:
            return self._original_func(*args, **kwargs)

    def _wrapped_func(self, args, kwargs, store, key, auto_close, open_kwargs):
        """
        Called by _func_by_position or _func_by_keyword if the file argument
        is given and file may need to be opened.
        """
        import io

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
    else:
        if isinstance(original_func, FileWrappedFunction):
            raise NotImplementedError("this decorator is not composable")
            # func = original_func
        else:
            func = FileWrappedFunction(original_func)
            func = functools.update_wrapper(func, original_func)
        func.add_filearg(filearg, auto_close, open_kwargs)
        return func
