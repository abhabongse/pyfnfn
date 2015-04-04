#!/usr/bin/env python3
#
# Author: Abhabongse Janthong <underneaththeunderneath@gmail.com>
# More info at https://github.com/abhabongse/python3-filewraps
#

def filewraps(input_func=None, *, filearg=0, auto_close=True, **open_kwargs):
  """Function wrapper that modifies the file argument to accept the filename
  string or the file descriptor integer in addition to file-like object."""

  import functools, inspect, operator, io

  if input_func is None:
    def decorator(input_func):
      return filewraps(input_func,
          filearg=filearg, auto_close=auto_close, **open_kwargs)
    return decorator
  else:
    # Actual wrapper that replaces the argument to file-like object.
    def replaced_output_func(args, kwargs, store, key):
      file = store[key]
      if isinstance(file, io.IOBase):
        return input_func(*args, **kwargs)
      elif auto_close:
        with open(file, **open_kwargs) as fobj:
          store[key] = fobj
          return input_func(*args, **kwargs)
      else:
        fobj = open(file, **open_kwargs)
        store[key] = fobj
        return input_func(*args, **kwargs)

    # Preprocessing the pseudo wrapper.
    sig = inspect.signature(input_func)
    spec = inspect.getfullargspec(input_func)
    try:
      filearg = spec.args[filearg]
    except TypeError:
      pass
    except IndexError as e:
      e.args = ("argument list index out of range",)
      raise e

    if filearg in spec.args:
      pos = spec.args.index(filearg)
      @functools.wraps(input_func)
      def output_func(*args, **kwargs):
        ba = sig.bind(*args, **kwargs)
        args, kwargs = list(ba.args), ba.kwargs
        if filearg in kwargs:
          return replaced_output_func(args, kwargs, kwargs, filearg)
        elif pos < len(args):
          return replaced_output_func(args, kwargs, args, pos)
        else:
          return input_func(*args, **kwargs)
      return output_func

    elif filearg in spec.kwonlyargs:
      @functools.wraps(input_func)
      def output_func(*args, **kwargs):
        ba = sig.bind(*args, **kwargs)
        args, kwargs = list(ba.args), ba.kwargs
        if filearg in kwargs:
          return replaced_output_func(args, kwargs, kwargs, filearg)
        else:
          return input_func(*args, **kwargs)
      return output_func

    else:
      raise NameError("{name} is not a valid argument for the function {func}"
          .format(name=str(filearg), func=input_func.__name__))
