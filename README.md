# Python Function Filename Wrapper

Python Function Filename Wrapper (`pyfnfn` for short; and formerly
`python-filewraps`) is a small `python` decorator snippet which extends any
`python` functions to accept **file names** as arguments in addition to
**file-like objects**.

This is a work in progress and should support `python3.3` and newer. For the
legacy version (including support for `python2.7` and `python3.2`), please see
[legacy/](legacy/).

## Testing and Examples of Usage

This project uses the built-in unittest module to test the implementation.
To run the test, execute the following command:

```bash
./runtest.sh
```

Also, in particular, the test file [test/test_wrapper.py](test/test_wrapper.py)
contains a few examples of how `@fnfnwrap` can be utilized.
