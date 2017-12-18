# Python Function Filename Wrapper

Python Function Filename Wrapper
(`pyfnfn` for short; and formerly `python-filewraps`)
is a small Python decorator snippet which extends the input entry point of
any Python functions to accept **file names** as input arguments given that
the function already accepts **file-like objects**.

This is a work in progress and should support `python3.4` and newer.
We dropped support for earlier versions of Python due to their support
reaching end-of-life.

The [earlier version (v0.6)](https://github.com/abhabongse/pyfnfn/tree/v0.6)
of `pyfnfn` also supports `python2.7`.

## Testing and Examples of Usage

This project uses the built-in unittest module to test the implementation.
To run the test, execute the following command:

```bash
./runtest.sh
```

Also, in particular, the test file
[test/test_wrapper.py](test/test_wrapper.py)
contains a few examples of how `@fnfnwrap` can be utilized.

## Important Note

In the future, I might actually adopt the very cool package called
[`wrapt` by Graham Dumpleton](https://github.com/GrahamDumpleton/wrapt)
instead of writing code from scratch. The code could have ended up much
simpler, and **it could be that everything in this package would break
in future versions**.
