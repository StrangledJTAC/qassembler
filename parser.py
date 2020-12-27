# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 13:43:07 2020

@author: JTAC
"""
import re
import error_classes as asm_err

opcodes_QCPU = {
    "MSC": "00000", "SST": "00001", "SLD": "00010", "SLP": "00011",
    "PST": "00100", "PLD": "00101", "CND": "00110", "LIM": "00111",
    "RST": "01000", "AST": "01001", "INC": "01010", "RSH": "01011",
    "ADD": "01100", "SUB": "01101", "XOR": "01110", "POI": "01111",
    "NOP": "100",   "JMP": "101",   "MST": "110",   "MLD": "111"}

symbol_table = {
    "$0": "000", "$1": "001", "$2": "010", "$3": "011", "$4": "100",
    "$5": "101", "$6": "110", "$7": "111"}

assembled_list = []


def preprocessor(lines):
    for line in lines:
        line = re.sub(r";.*", "", line)  # strip comments
    lines = [line for line in lines if line != ""]   # remove empty lines
    lines = [line.strip() for line in lines]  # strip head and tail whitespace
    return lines


def data_parse(data, line_num):  # handles immediate values
    data = re.match(r"\d+", data)
    if data is not None:
        data = data.group()
        if data in range(256):
            return "{0:b}".format(data).zfill(8)  # returns 8-bit binary integer
        else:
            raise asm_err.AssemblerRangeError(line_num, "Value out of range: 0 - 255")
    else:
        raise asm_err.AssemblerSyntaxError(line_num, "Unrecognized Symbol")


def operand_parse(operand, line_num, machine_op):
    bits_remain = 8 - len(machine_op)
    if bits_remain == 3:
        register = re.match(r"(<=[a-zA-z]*3\w+)\$\d)", operand)
        if register is not None:
            register = symbol_table.get(register.group())
            if register is None:
                raise asm_err.AssemblerRangeError(line_num, "Register address out of bounds: $0 - $7")
            elif


def parser(lines):  # parser control function
    for line_num, line in enumerate(lines, start=1):
        opcode = re.match(r"[a-zA-z]*3", line)
        if opcode is not None:
            machine_op = opcodes_QCPU.get(opcode.group())
            operand = operand_parse(line, line_num, machine_op)
        else:
            data = data_parse(line, line_num)
            assembled_list[line_num] = data
            continue
