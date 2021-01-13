# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 13:43:07 2020

@author: JTAC
"""
import re
import error_classes as asm_err
import symbol_table
import sys

assembled_list = []


def preprocessor(infile):
    try:
        with open(infile, 'r') as asm:
            lines = asm.readlines()
    except FileNotFoundError:
        sys.exit("File does not exist or path is incorrect.")

    # strip comments, remove empty lines, and unnecessary whitespace
    lines = [re.sub(r"[;/].*", "", line) for line in lines]
    lines = [line for line in lines if line != ""]
    lines = [line.strip() for line in lines]
    return lines


class parser:
    def __init__(self, source):
        self.source = preprocessor(source)
        self.current_command = ""
        self.lindex = 0

    def hasMoreCommands(self):
        if self.lindex == len(self.source):
            return False
        else:
            return True

    def advance(self):
        self.current_command = self.source[self.lindex]
        self.lindex += 1

    def reset(self):  # resets parser for second pass
        self.lindex = 0
        self.current_command = ""
        for count, line in enumerate(self.source):
            if re.match(r"[a-zA-Z\._][a-zA-Z\._0-9]*(?=:)", line):
                del self.source[count]  # remove labels

    def commandType(self):
        if re.match(r"[a-zA-Z\._][a-zA-Z\._0-9]*:", self.current_command):
            return "label"
        elif re.match(r"\d+", self.current_command):
            return "data"
        else:
            return "operation"

    def data(self):
        data = int(re.match(r"\d+", self.current_command).group())
        if data in range(256):
            return "{0:b}".format(data).zfill(8)  # returns 8-bit binary data
        else:
            raise asm_err.AssemblerRangeError(self.lindex, "Value out of range: 0 - 255")

    def label(self):
        label = re.match(r"[a-zA-Z\._][a-zA-Z\._0-9]*(?=:)", self.current_command)
        return label.group()

    def operation(self):
        opcode = re.match(r"[A-Z]{3}", self.current_command).group()
        if opcode is None:
            raise asm_err.AssemblerSyntaxError(self.lindex, "Unrecognized Instruction.")
        else:
            return opcode

    def operand(self):
        bits_remain = 8 - len(self.operation())
        if bits_remain == 3:
            register = re.match(r"(<=[a-zA-z]*3\w+)\$\d)", self.current_command)
            if register is not None:
                register = symbol_table.GetAddress(register.group())
            if register is None:
                raise asm_err.AssemblerRangeError(self.lindex, "Register address out of bounds: $0 - $7")
