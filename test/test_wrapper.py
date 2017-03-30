#!/usr/bin/env python3
# Author: Abhabongse Janthong <underneaththeunderneath@gmail.com>
# More info at https://github.com/abhabongse/pyfnfn
"""Test suite for Python Function Filename Wrapper. It also serves as examples
of how the usage of `@fnfnwrap` is intended.
"""
__all__ = ()

import os
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

# TODO: testing error handlings
# TODO: testing writing files
# TODO: testing with default argument values
# TODO: testing with object, class, and static methods
# TODO: testing with composite wraps

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

if __name__ == '__main__':
    unittest.main()
