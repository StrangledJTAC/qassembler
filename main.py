# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 02:00:26 2020

@author: JTAC
"""
import re
import sys
import parser


def main():
    infile = str(sys.argv[1])
    try:
        with open(infile, 'r') as asm:
            lines = asm.readlines()
    except IOError:
        print("File does not exist or path is incorrect.")
        exit(1)

    cleaned_file = parser.preprocessor(lines)
    first_pass = parser.parser(cleaned_file)
