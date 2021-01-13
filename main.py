# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 02:00:26 2020

@author: JTAC

LABEL support: Yes
VARIABLE support: No (reason: hardware precludes necessary memory protection)
"""
#!/usr/bin/env python

import sys
import qasm_parser
import qasm_code
import qsymbol_table
import error_classes as asm_error

assembled_list = []


def main():
    try:
        infile = str(sys.argv[1])
    except IndexError:
        sys.exit("Usage: qas filename")

    # First Pass: Collect all labels and add them to symbol table
    first = qasm_parser.parser(infile)  # initialize parser object
    symbolizer = qsymbol_table.symbolizer()  # initialize symbolizer object
    while first.hasMoreCommands():
        first.advance()
        if first.commandType() == 'label':
            if symbolizer.contains(first.label()) is False:
                symbolizer.addEntry(first.label(), first.lindex - 1)
            else:
                reason = "Label defined more than once"
                raise asm_error.AssemblerSyntaxError(first.lindex, reason)

    print(symbolizer.symbol_table)
    print(first.source)
    print(first.lindex, '\n')
    # Reset parser and exclude label definitions from further analysis
    first.reset()
    if len(first.source) > 31:
        raise asm_error.AssemblerMemoryError("maximum 32 bytes")
    print(symbolizer.symbol_table)
    print(first.source)
    print(first.lindex)
    # Second Pass: Collect instructions and generate machine code

    generator = qasm_code.generator()  # initialize code generator object
    while first.hasMoreCommands():
        first.advance()
        if first.commandType() == 'data':
            assembled_list.append(first.data())
        elif first.commandType() == 'operation':
            opcode = generator.code(first.operation())
            assembled_list.append(opcode[0])

main()
