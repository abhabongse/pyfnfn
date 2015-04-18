# python-filewraps

`python-filewraps` is a small `python` decorator snippet which extends any `python` functions to accept **file names** as arguments in addition to **file-like objects**. It was originally written for personal day-to-day usage and it works on both `python2` as well as `python3` (only tested on `python2.7` and `python3.4`). It is released under [MIT License](LICENSE).


## Getting started

First, copy `filewraps.py` file to any location in your project where it could be imported. From within your python source file, simply import `filewraps` from the `filewraps` module and apply it as the decorator `@filewraps` to any function definition you write.

You may see (outdated) examples of how to user `filewraps` at [example2.py](./example2.py) for `python2` and at [example3.py](./example3.py) for `python3`. For the actual documentation, see the next section.


## Documentation

The signature of the decorator `filewraps` is

```python
def filewraps(original_func=None, filearg=0, auto_close=True, **open_kwargs):
```

For more details about each argument, check out subtopics below.

### 1. Decorators

The first argument `original_func` is a function you wish to add the capability of accepting file names as arguments in addition to file-like objects, without modifying the original code. The function `original_func` will be wrapped under a new callable object that will be returned as the output of `filewraps`.

The following two examples are equivalent: they both return the first line of a given file. Note that the latter examples shows how `filewraps` is used as a decorator to a function definition.

```python
def read_first_line(f):
  return f.readline()
read_first_line = filewraps(read_first_line)
```

```python
@filewraps  # using as decorator
def read_first_line(f):
  return f.readline()
```

### 2. Specifying file argument

The second argument `filearg` specifies which argument of `original_func` should be watched for file names in addition to file-like objects. It can either be

- an integer, possibly negative, specifying the 0-index positional argument of `original_func`, or

- a string representing the argument name of the `original_func`.

The _default value_ of `filearg` is `0` which means that the _first_ argument of `original_func` is expected to receive file-like object by default (as in the above two examples).

Here are three example that are semantically equivalent: they all return the first `l` lines of a given file.

```python
@filewraps(filearg=1)
def read_first_l_lines(l, f):
  return f.readlines()[:l]
```

```python
@filewraps(filearg=-1)
def read_first_l_lines(l, f):
  return f.readlines()[:l]
```

```python
@filewraps(filearg='f')
def read_first_l_lines(l, f):
  return f.readlines()[:l]
```

### 3. Auto closing files

Another argument called `auto_close` is a boolean indicating whether a file specified in the file argument should be closed automatically after the execution of `original_func` has ended. This option only applies to cases when the file argument is provided as a file name by the caller, which causes the file to be opened while the function is called. In other words, if the caller provided a file-like object to the function, this option will be ignored, and the file-like object will **never be closed automatically**.

Here is how files are closed automatically by default when the file argument is provided as a file name. `False` and `True` are printed respectively.

```python
@filewraps
def return_file_object(f):
  print(f.closed)
  return f  # In reality, you should never do this.

f = return_file_object('input.txt')
print(f.closed)
```

So how does setting `auto_close` to `False` come in handy? Consider the following example: if your function is going to be a generator, you need to set `auto_close` to `False` to prevent premature file closing.

```python
@filewraps(auto_close=False)
def read_each_integer(f):
  for line in f:
    for token in line.split():
      yield int(token)  # creates a generator and return each integer one by one
  f.close()  # at the end of iteration, manually close the file
```

### 4. Optional arguments of `open()`

The last keyword variable `open_kwargs` is a dictionary of keyword arguments that will be used as arguments of `open()` when opening the file from a given file name. The most common usage is to specify the mode of the file to writing instead of reading. For example,

```python
@filewraps(filearg='f', mode='w')
def write_integer(num, f):
  print(num, file=f)
```

## Frequently asked questions

#### Can I provide a default value for the file argument of a function that I write?

Sure. For example, you may want to read an input from standard input whenever a file name is not given.

```python
@filewraps
def read_first_line(f=sys.stdin):
  return f.readline()
```

#### Does this code work with keyword-only arguments in `python3`?

Of course. This project was initially aimed at `python3` only, so the support for keyword-only arguments is carefully considered.

#### Does this decorator snippet work with `python2` as well?

<del>No. The simple reason is that the language specification for functions in `python2` and `python3` are different: `python2` does not accept keyword-only arguments while `python3` does. For the argument `filearg` to support keyword-only arguments in `python3`, compatibility with `python2` has to be dropped</del>.

<del>Another reason is that I want to support the advancement towards adopting `python3`. Although the library could be easily modified to support `python2`, I will never do it myself in a thousand years. But, of course, you are welcome to do it yourself and share it to the world. It's FOSS after all</del>.

Yes.

#### Are `@filewraps` decorators composable?

Not yet. I will add this feature in not-so-near future. Whenever I need this feature myself, I will add it. But no, definitely not soon.

The reason why they are not composable is that the **signature** of the input function to `filewraps` is **not preserved** in the output, while `filewraps` at the same time needs to inspect the signature of the input function. So a function cannot be wrapped with `filewraps` more than once.

There are two ways to fix this:

1.  Implement the missing part in the code by yourself. You will be suprised to see that the code already allows extra file arguments to be added.

2.  Use PyPI package [`decorator`](https://pypi.python.org/pypi/decorator) so that functions returned by `@filewraps` decorator preserve their signature. I haven't test it yet but it should work.

#### I have a suggestion for improvement and a pull req&mdash; ####

Of course. Not sure how pull requests work, so you will need to help me out too :P
