#!/usr/bin/env python

import string
import fileinput
import sys

printable = set(string.printable)

for line in fileinput.input():
    sys.stdout.write((filter(lambda x : x in printable, line.decode('latin1')).encode('ascii')))
