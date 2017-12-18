#!/usr/bin/env python3
# Author: Abhabongse Janthong
# More info at https://github.com/abhabongse/pyfnfn
"""Test suite for Python Function Filename Wrapper. It also serves as examples
of how the usage of `@fnfnwrap` is intended.
"""
__all__ = ()

import io
import os
import tempfile
import textwrap
import unittest
from pyfnfn import fnfnwrap

# Obtain the path for data.txt within the same directory as this code.
this_dir = os.path.dirname(os.path.abspath(__file__))
data_filename = os.path.join(this_dir, 'data.txt')

# Extract the numbers for reference.
with open(data_filename) as data_file:
    ref_data = [ int(token) for line in data_file for token in line.split() ]

##################################################################
##  1. Default usage for decorator
##################################################################

@fnfnwrap
def read_numbers_default(file_input):
    extracted_data = []
    for line in file_input:
        for token in line.split():
            extracted_data.append(int(token))
    return extracted_data

##################################################################
##  2. Three different usages that are semantically equivalent:
##  Indexing for positional arguments and variable names are all
##  accepted as filearg specifiers. First two arguments, namely
##  `start_message` and `end_message` are for illustrative
##  purposes so they are ignored in the function bodies.
##################################################################

@fnfnwrap(filearg=2)  # positional argument 2
def read_numbers_nonnegative_index(start_message, end_message, file_input):
    return [ int(token) for line in file_input for token in line.split() ]

@fnfnwrap(filearg=-1)  # positional argument -1
def read_numbers_negative_index(start_message, end_message, file_input):
    return [ int(token) for line in file_input for token in line.split() ]

@fnfnwrap(filearg='file_input')  # named argument 'file_input'
def read_numbers_named_filearg(start_message, end_message, file_input):
    return [ int(token) for line in file_input for token in line.split() ]

##################################################################
##  3. Function filename wrapper also works with keyword-only
##  but filearg must then be specified as named arguments.
##################################################################

@fnfnwrap(filearg='data_input')
def read_numbers_keyword_only(*, data_input):
    return [ int(token) for line in data_input for token in line.split() ]

##################################################################
##  4. Decorator could be used on generator functions as well.
##  The tricky part of the implementation is that the wrapper
##  function must also be a generator function because we would
##  like to use with-statement to open and close files cleanly,
##  and thus would make sure that the execution of the generator
##  is halted without kicking in the context manager clean-up
##  process that would prematurely closes the file.
###################################################################

@fnfnwrap
def read_numbers_generator(file_input):
    count = 0
    for line in file_input:
        for token in line.split():
            yield int(token)
            count += 1
    return count

##################################################################
##  5. In order to open files are writing instead of reading,
##  the decorator could specify the mode (among other
##  arguments) to `open()`` function. Also, the example below
##  demonstrates how filearg allows default values.
##  Note: to make this function testable, we wrap the main
##  function inside another function to init `default_file`
##  so that it is defined right before when it is called.
##################################################################

def construct_and_run(content, default_file, called_file=None):
    with open(default_file, mode='w') as fileobj:
        ##########################################
        # HERE IS THE ACTUAL FUNCTION IN PRACTICE
        # In fact, the default could have been
        # standard input/output/error or so.
        ##########################################
        @fnfnwrap(filearg='file_output', mode='w')
        def write_hello(message, file_output=fileobj):
            print(message, file=file_output)
        ##########################################
        # FUNCTION ENDS HERE
        ##########################################
        if called_file:
            write_hello(content, called_file)
        else:
            write_hello(content)

##################################################################
##  6. It is possible to use decorator on the same function
##  twice in the composition manner, as shown below. Notice that
##  the function docstring is also preserved in the end.
##################################################################

@fnfnwrap(filearg=0)
@fnfnwrap(filearg=1, mode='w')
def copy_integers(source_file, dest_file):
    """\
    Copy the sequence of integers from one file to the other without
    having to preserve the structure.
    """
    for line in source_file:
        for token in line.split():
            print(int(token), file=dest_file)

##################################################################
##  7. Exception during the function definition is shown in
##  the construction of the `unittest.TestCase`.
##################################################################

pass

##################################################################
##  8. This example demonstrates how the decorator could be
##  used with method in classes.
##################################################################

class DataCollection(object):
    def __init__(self, file_input):
        self._populate(file_input)
    @fnfnwrap(filearg='file_input')
    def _populate(self, file_input):
        self.data = [
            int(token)
            for line in file_input for token in line.split()
            ]
    def __iter__(self):
        return iter(self.data)

###################################
##  All test cases resides here  ##
###################################

class FnFnWrapTestCase(unittest.TestCase):

    def test_default_usage(self):
        self.assertEqual(read_numbers_default(data_filename), ref_data)
        with open(data_filename) as data_file:
            self.assertEqual(read_numbers_default(data_file), ref_data)

    def test_filearg_usage(self):
        for func in (read_numbers_nonnegative_index,
                   read_numbers_negative_index,
                   read_numbers_named_filearg):
            with self.subTest(func=func.__qualname__):
                self.assertEqual(func('A', 'B', data_filename), ref_data)
                with open(data_filename) as data_file:
                    self.assertEqual(func('A', 'B', data_file), ref_data)

    def test_keyword_only_filearg(self):
        self.assertEqual(read_numbers_keyword_only(data_input=data_filename),
                         ref_data)
        with open(data_filename) as data_file:
            self.assertEqual(read_numbers_keyword_only(data_input=data_file),
                             ref_data)

    def test_generator(self):
        try:
            sequence = read_numbers_generator(data_filename)
            for x, y in zip(sequence, ref_data):
                self.assertEqual(x, y)
        except StopIteration as e:
            self.assertEqual(e.value, len(ref_data))
        try:
            with open(data_filename) as data_file:
                sequence = read_numbers_generator(data_file)
                for x, y in zip(sequence, ref_data):
                    self.assertEqual(x, y)
        except StopIteration as e:
            self.assertEqual(e.value, len(ref_data))

    def test_write_files(self):
        with tempfile.TemporaryDirectory() as tempdir:
            f1 = os.path.join(tempdir, 'one.txt')
            f2 = os.path.join(tempdir, 'two.txt')
            f3 = os.path.join(tempdir, 'three.txt')

            def assertFileEqual(file_name, expected_content):
                with open(file_name) as file_obj:
                    self.assertEqual(file_obj.read().strip(), expected_content)

            construct_and_run('one', f1)
            assertFileEqual(f1, 'one')

            construct_and_run('two', f1, f2)
            assertFileEqual(f1, '')
            assertFileEqual(f2, 'two')

            with open(f3, 'w') as file_obj:
                construct_and_run('three', f1, file_obj)
            assertFileEqual(f1, '')
            assertFileEqual(f2, 'two')
            assertFileEqual(f3, 'three')

    def test_composite_decorator(self):
        with tempfile.TemporaryDirectory() as tempdir:
            f1 = os.path.join(tempdir, '1.txt')
            f2 = os.path.join(tempdir, '2.txt')
            f3 = os.path.join(tempdir, '3.txt')
            f4 = os.path.join(tempdir, '4.txt')

            copy_integers(data_filename, f1)
            self.assertEqual(read_numbers_default(f1), ref_data)

            with open(data_filename) as data_file:
                copy_integers(data_file, f2)
            self.assertEqual(read_numbers_default(f2), ref_data)

            with open(f3, mode='w') as f3_obj:
                copy_integers(data_filename, f3_obj)
            self.assertEqual(read_numbers_default(f3), ref_data)

            with open(data_filename) as data_file, \
                 open(f4, mode='w') as f4_obj:
                copy_integers(data_file, f4_obj)
            self.assertEqual(read_numbers_default(f4), ref_data)

    def test_docstring_preservation(self):
        main_string = textwrap.dedent(copy_integers.__doc__)
        expected_string = textwrap.dedent("""\
            Copy the sequence of integers from one file to the other without
            having to preserve the structure.
            """)
        self.assertEqual(main_string, expected_string)

    def test_exceptions(self):
        with self.assertRaisesRegex(
                TypeError, r'expected a callable function'):
            fnfnwrap(1)
        with self.assertRaisesRegex(
                IndexError, r'argument list index out of range'):
            @fnfnwrap
            def dummy(): pass
        with self.assertRaisesRegex(
                IndexError, r'argument list index out of range'):
            @fnfnwrap(filearg=3)
            def dummy(a, b, c): pass
        with self.assertRaisesRegex(
                IndexError, r'argument list index out of range'):
            @fnfnwrap(filearg=-2)
            def dummy(x): pass
        with self.assertRaisesRegex(
                NameError, r'not a valid argument for the function'):
            @fnfnwrap(filearg='z')
            def dummy(a, b, c): pass
        with self.assertRaisesRegex(
                TypeError, r'has incorrect type'):
            @fnfnwrap(filearg=b'a')
            def dummy(a, b, c): pass
        with self.assertRaisesRegex(
                TypeError, r'not a valid argument for built-in function open'):
            @fnfnwrap(filearg=0, modal=10)
            def dummy(a, b, c): pass
        with self.assertRaisesRegex(
                TypeError, r'unrecognized type for filename or file object'):
            read_numbers_default(10)

    def test_function_methods(self):
        data_v1 = DataCollection(data_filename)
        self.assertEqual(list(data_v1), ref_data)
        with open(data_filename) as data_file:
            data_v2 = DataCollection(data_file)
        self.assertEqual(list(data_v2), ref_data)


if __name__ == '__main__':
    unittest.main()
