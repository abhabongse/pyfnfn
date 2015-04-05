# python3-filewraps

`python3-filewraps` is a small `python3` decorator snippet which extends any `python3` functions to accept _file name_ as arguments in addition to _file-like objects_. It was originally written for personal day-to-day usage, and it is released under [MIT License](LICENSE).


## Getting started

First, copy `python3_filewraps.py` file to any location in your project where it could be imported. From within your python source file, simply import `filewraps` from the `python3_filewraps` module and apply it as the decorator `@filewraps` to any function definition you write.

Few examples of how to use `@filewraps` could be seen at [example.py](./example.py). For the actual documentation, see below.


## Documentation

The signature of the decorator `@filewraps` is

**`filewraps(input_func=None, *, filearg=0, auto_close=True, **open_kwargs)`**

For more details about each argument, check out subtopics below.

### 1. Decorators

The first­ and the only positional argument `input_func` is a function you wish to add the capability of accepting file names as arguments in addition to file-like objects. The function `input_func` will be wrapped and returned as the output of `filewraps`.

The following two examples are equivalent: they all return the first line of a given file.

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

The keyword-only argument `filearg` specifies which argument of `input_func` should be watched for file names in addition to file-like objects. It can either be

- an integer specifying the 0-index of the position argument of `input_func`, or

- a string representing the argument name of the `input_func`.

The default value of `filearg` is `0` which means that the *first* argument of `input_func` is expected to receive file-like object by default (as in the above two examples).

Here are three example that are semantically equivalent: they all return the first `l` lines of a given file:

```python
@filewraps(filearg=1)
def read_first_l_lines(l, f):
  return f.readlines()[:l]
```

```python
@filewraps(filearg=-1)  # Yes, negative index also allowed.
def read_first_l_lines(l, f):
  return f.readlines()[:l]
```

```python
@filewraps(filearg='f')
def read_first_l_lines(l, f):
  return f.readlines()[:l]
```

### 3. Auto closing files

Another keyword-only argument `auto_close` is a boolean indicating whether a file argument should be closed automatically once the execution of `input_func` is done. This option has an effect only when the file argument is initially specified as file name strings (not as file-like objects).

In other words, the file-like object will **never** be closed regardless of the boolean value of `auto_close` if it is initially specified as file-like object itself. Here is some demonstration:

```python
@filewraps
def return_file_object(f):
  return f  # in reality, you should never do this

f1 = do_nothing('input.txt')
f1.closed  # return True

with open('input.txt') as fobj:
  f2 = do_nothing('input.txt')
  f2.closed  # return False
f2.closed # return True
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

#### Does this decorator snippet work with `python2` as well?

No. The simple reason is that the language specification for functions in `python2` and `python3` are different: `python2` does not accept keyword-only arguments while `python3` does. For the argument `filearg` to support keyword-only arguments in `python3`, compatibility with `python2` has to be dropped.

Another reason is that I want to support the advancement towards adopting `python3`. Although the library could be easily modified to support `python2`, I will never do it myself in a thousand years. But, of course, you are welcome to do it yourself and share it to the world. It's FOSS after all.

#### Is the decorator `@filewraps` composable?

Not yet. I will add this feature in not-so-near future. Whenever I need this feature myself, I will add it. But no, definitely not soon.

#### Why is it not composable?

It is because the signature of the input function to `filewraps` is not preserved in the output, while `filewraps` at the same time needs to inspect the signature of the input function. So a function cannot be wrapped with `filewraps` more than once.

#### I have a suggestion for improvement and a pull req&mdash; ####

Of course. Not sure how pull requests work, so you will need to help me out too :P
