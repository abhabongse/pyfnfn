#!/usr/bin/env python2
#
# Author: Abhabongse Janthong <underneaththeunderneath@gmail.com>
# More info at https://github.com/abhabongse/python3-filewraps
#

import sys
import itertools
from filewraps import filewraps

#
# Example 1
# Default use of @filewraps, the first (index 0) positional
# argument is expected to accept a file-like object.
#
print "Example 1"


@filewraps
def read_file(file=sys.stdin, l=4):
    """Print the first l lines of the input file."""
    for index, line in enumerate(itertools.islice(file, l), start=1):
        print "Line {}: {}".format(index, line.strip())
    print "Stop."

read_file()  # Read the first 4 lines from standard input.
read_file(l=6)  # Read the first 6 lines from standard input.
read_file('input.txt')  # Read the first 4 lines from the file.
read_file('input.txt', 6)  # Read the first 6 lines from the file.
read_file(l=6, file='input.txt')  # Read the first 6 lines from the file.


#
# Example 2
# Specify the file argument by 0-index position of the positional
# arugments.
#
print "Example 2"


@filewraps(filearg=2)
def read_file(max_lines=4, max_length=5, file=sys.stdin):
    """Print the first `max_lines` lines of the input file,
    limiting each line to `max_length` characters."""
    for index, line in enumerate(itertools.islice(file, max_lines), start=1):
        output = ''.join(itertools.islice(line.strip(), max_length))
        print "Line {}: {}".format(index, output)
    print "Stop."

read_file()  # Read 5 chars of first 4 lines from standard input.
read_file(2, 7)  # Read 7 chars of first 2 lines from standard input.
read_file(3, 4, 'input.txt')  # Read 4 chars of first 3 linrs from the file.


#
# Example 3.
# Negative indexing also works.
#
print "Example 3"


@filewraps(filearg=-1)
def read_file(max_lines=4, max_length=5, file=sys.stdin):
    """Print the first `max_lines` lines of the input file,
    limiting each line to `max_length` characters."""
    for index, line in enumerate(itertools.islice(file, max_lines), start=1):
        output = ''.join(itertools.islice(line.strip(), max_length))
        print "Line {}: {}".format(index, output)
    print "Stop."

read_file()  # Read 5 chars of first 4 lines from standard input.
read_file(2, 7)  # Read 7 chars of first 2 lines from standard input.
read_file(3, 4, 'input.txt')  # Read 4 chars of first 3 lines from the file.


#
# Example 4.
# Instead of using integer indexing, we can specify the argument name.
# Also, in the same example, we will disable file auto close so that
# the function is allowed to become a generator.
#
print "Example 4"


@filewraps(filearg='file', auto_close=False)
def read_file(file):
    """Read the entire file and print."""
    for index, line in enumerate(file, start=1):
        print "Line {}: {}".format(index, line.strip())
    print "Stop."

read_file('input.txt')


#
# Example 5.
# Use the @filewraps to open the files for writing.
#
print("Example 5")


@filewraps(filearg='file', mode='w')
def write_file(text, file=sys.stdout):
    """Write the text to the file."""
    file.write(text + "\n")

write_file("Hello.")
write_file("Hi.", 'output.txt')
