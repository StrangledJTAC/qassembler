# -*- coding: utf-8 -*-

class generator:
    def __init__(self):
        self.code_table = {
         "MSC": ("00000", '-n'), "SST": ("00001", '-i'),
         "SLD": ("00010", '-i'), "SLP": ("00011", '-i'),
         "PST": ("00100", '-i'), "PLD": ("00101", '-i'),
         "CND": ("00110", '-c'), "LIM": ("00111", '-r'),
         "RST": ("01000", '-r'), "AST": ("01001", '-r'),
         "INC": ("01010", '-r'), "RSH": ("01011", '-r'),
         "ADD": ("01100", '-r'), "SUB": ("01101", '-r'),
         "XOR": ("01110", '-r'), "POI": ("01111", '-r'),
         "NOP": ("100", '-n'), "JMP": ("101", '-l'),
         "MST": ("110", '-m'), "MLD": ("111", '-m')}

    def code(self, mnemonic):
        return self.code_table[mnemonic]
