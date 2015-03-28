#!/usr/bin/env python3
# Abhabongse Janthong <underneaththeunderneath@gmail.com>
# File wrapper utility.

import functools, inspect, operator, io

def filewraps(wrapped=None, *, filearg=0, auto_close=True, **open_kwargs):
  """Function wrapper that modifies the file argument to accept the filename
  string or the file descriptor integer in addition to file-like object."""

  if wrapped is None:
    def decorator(wrapped):
      return filewraps(wrapped,
          filearg=filearg, auto_close=auto_close, **open_kwargs)
    return decorator
  else:
    # Actual wrapper that replaces the argument to file-like object.
    def replace_wrapper(args, kwargs, store, key):
      file = store[key]
      if isinstance(file, io.IOBase):
        return wrapped(*args, **kwargs)
      elif auto_close:
        with open(file, **open_kwargs) as fobj:
          store[key] = fobj
          return wrapped(*args, **kwargs)
      else:
        fobj = open(file, **open_kwargs)
        store[key] = fobj
        return wrapped(*args, **kwargs)

    # Preprocessing the pseudo wrapper.
    sig = inspect.signature(wrapped)
    spec = inspect.getfullargspec(wrapped)
    try:
      filearg = spec.args[filearg]
    except TypeError:
      pass
    except IndexError as e:
      e.args = ("argument list index out of range",)
      raise e

    if filearg in spec.args:
      pos = spec.args.index(filearg)
      @functools.wraps(wrapped)
      def wrapper(*args, **kwargs):
        ba = sig.bind(*args, **kwargs)
        args, kwargs = list(ba.args), ba.kwargs
        if filearg in kwargs:
          return replace_wrapper(args, kwargs, kwargs, filearg)
        elif pos < len(args):
          return replace_wrapper(args, kwargs, args, pos)
        else:
          return wrapped(*args, **kwargs)
      return wrapper

    elif filearg in spec.kwonlyargs:
      @functools.wraps(wrapped)
      def wrapper(*args, **kwargs):
        ba = sig.bind(*args, **kwargs)
        args, kwargs = list(ba.args), ba.kwargs
        if filearg in kwargs:
          return replace_wrapper(args, kwargs, kwargs, filearg)
        else:
          return wrapped(*args, **kwargs)
      return wrapper

    else:
      raise NameError("{name} is not a valid argument for the function {func}"
          .format(name=str(filearg), func=wrapped.__name__))
