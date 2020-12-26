# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 13:43:07 2020

@author: JTAC
"""
import re

opcodes_QCPU = {
    "NOP": "00000", "SST": "00001", "SLD": "00010", "SLP": "00011",
    "PST": "00100", "PLD": "00101", "CND": "00110", "LIM": "00111",
    "RST": "01000", "AST": "01001", "INC": "01010", "RSH": "01011",
    "ADD": "01100", "SUB": "01101", "XOR": "01110", "POI": "01111",
    "DIM": "100",   "JMP": "101",   "MST": "110",   "MLD": "111"}

symbol_table = {
    "$0": "000", "$1": "001", "$2": "010", "$3": "011", "$4": "100",
    "$5": "101", "$6": "110", "$7": "111"}

assembled_list = []


def preprocessor(lines):
    for line in lines:
        line = re.sub(r"\w*//.*", "", line)  # strips comments
    lines = list(filter(lambda line: line != ""))   # remove empty lines
    lines = [line.strip() for line in lines]  # strips head and tail whitespace
    return lines


def data_parse(data):  # handles immediate values
    data = re.match(r"\d+", data)


def parser(lines):
    for line in lines:
        opcode = re.match(r"[a-zA-z]*3", line)
        if opcode is not None:
            machine_op = opcodes_QCPU.get(opcode.group())
        else:
            data_parse(line)

