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

######################################
##  I. Default usage for decorator  ##
######################################

@fnfnwrap
def read_numbers_default(file_input):
    extracted_data = []
    for line in file_input:
        for token in line.split():
            extracted_data.append(int(token))
    return extracted_data

###################################################################
##  II. Three different usages that are semantically equivalent  ##
##      `start_message` and `end_message` are for illustrative   ##
##      purpose so they are ignored in the following functions   ##
###################################################################

@fnfnwrap(filearg=2)  # positional argument 2
def read_numbers_nonnegative_index(start_message, end_message, file_input):
    extracted_data = [
        int(token)
        for line in file_input for token in line.split()
        ]
    return extracted_data

@fnfnwrap(filearg=-1)  # positional argument -1
def read_numbers_negative_index(start_message, end_message, file_input):
    extracted_data = [
        int(token)
        for line in file_input for token in line.split()
        ]
    return extracted_data

@fnfnwrap(filearg='file_input')  # named argument 'file_input'
def read_numbers_named_filearg(start_message, end_message, file_input):
    extracted_data = [
        int(token)
        for line in file_input for token in line.split()
        ]
    return extracted_data

# TODO: testing generators
# TODO: testing error handlings
# TODO: testing writing files
# TODO: testing with default argument values

###################################
##  All test cases resides here  ##
###################################

class FnFnWrapTestCase(unittest.TestCase):

    def test_default_usage(self):
        "@fnfnwrap with default settings"
        self.assertEqual(read_numbers_default(data_filename), ref_data)
        with open(data_filename) as data_file:
            self.assertEqual(read_numbers_default(data_file), ref_data)

    def test_filearg_usage(self):
        "@fnfnwrap with filearg specified in three different ways"
        for func in (read_numbers_nonnegative_index,
                   read_numbers_negative_index,
                   read_numbers_named_filearg):
            with self.subTest(func=func.__qualname__):
                self.assertEqual(func('A', 'B', data_filename), ref_data)
                with open(data_filename) as data_file:
                    self.assertEqual(func('A', 'B', data_file), ref_data)

if __name__ == '__main__':
    unittest.main()
