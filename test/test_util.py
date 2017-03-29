#!/usr/bin/env python3
# Author: Abhabongse Janthong <underneaththeunderneath@gmail.com>
# More info at https://github.com/abhabongse/pyfnfn
"""Test suite for Python Function Filename Wrapper. It also serves as examples
of how the usage of `@fnfnwrap` is intended.
"""
__all__ = ()

import itertools
import os
import sys
import unittest
from pyfnfn.util import is_valid_filename, check_open_kwargs

# Obtain the path for data.txt within the same directory as this code.
this_dir = os.path.dirname(os.path.abspath(__file__))
data_filename = os.path.join(this_dir, 'data.txt')

#########################################################
##  All test cases for is_valid_filename resides here  ##
#########################################################

class ValidFilenameTestCase(unittest.TestCase):

    def test_str(self):
        self.assertTrue(is_valid_filename('a string is okay'))
        self.assertTrue(is_valid_filename('another string'))
        self.assertTrue(is_valid_filename(''))  # empty string included

    def test_bytes(self):
        self.assertTrue(is_valid_filename(b'a string is okay'))
        self.assertTrue(is_valid_filename(b'another string'))
        self.assertTrue(is_valid_filename(b''))  # empty string included

    @unittest.skipIf(sys.version_info < (3, 6), 'requires python3.6+')
    def test_pathlike_object(self):
        from pathlib import Path
        self.assertTrue(is_valid_filename(Path('.')))
        self.assertTrue(is_valid_filename(Path('new-file')))
        self.assertTrue(is_valid_filename(Path('directory/new-file')))

    def test_invalid_filenames(self):
        self.assertFalse(is_valid_filename(12))
        self.assertFalse(is_valid_filename(-3.4))
        self.assertFalse(is_valid_filename(True))
        self.assertFalse(is_valid_filename(False))
        self.assertFalse(is_valid_filename(None))
        with open(data_filename) as data_file:
            self.assertFalse(is_valid_filename(data_file))
        self.assertFalse(is_valid_filename(lambda: None))


#########################################################
##  All test cases for check_open_kwargs resides here  ##
#########################################################

class ValidOpenKeywordArgumentsTestCase(unittest.TestCase):

    def test_valid_open_arguments(self):
        try:
            # Hard code to avoid the same pitfall as the implementation
            valid_args = ('mode', 'buffering', 'encoding', 'errors',
                          'newline', 'closefd', 'opener')
            powerset_args = itertools.chain.from_iterable(
                itertools.combinations(valid_args, r)
                for r in range(len(valid_args) + 1)
                )
            for subset_args in powerset_args:
                open_kwargs = { arg: None for arg in subset_args }
                check_open_kwargs(open_kwargs)
        except:
            self.fail('Exception raised unexpectedly!')

    def test_invalid_open_arguments(self):
        with self.assertRaises(TypeError):
            check_open_kwargs({'modal': None})
        with self.assertRaises(TypeError):
            valid_args = ('mode', 'buffering', 'encoding', 'errors',
                          'newline', 'closefd', 'opener')
            open_kwargs = { arg: None for arg in valid_args }
            open_kwargs['wrong'] = None
            check_open_kwargs(open_kwargs)
