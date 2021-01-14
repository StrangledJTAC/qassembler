class Symbolizer:
    def __init__(self):
        self.symbol_table = {
         "$0": "000", "$1": "001", "$2": "010", "$3": "011", "$4": "100",
         "$5": "101", "$6": "110", "$7": "111"}

    def addEntry(self, symbol, address):
        self.symbol_table[symbol] = address

    def contains(self, symbol):
        return bool(symbol in self.symbol_table)

    def getAddress(self, symbol):
        return self.symbol_table[symbol]


class Generator:
    def __init__(self):
        self.code_table = {
         "MSC": ("00000", '-n'), "SST": ("00001", '-d'),
         "SLD": ("00010", '-d'), "SLP": ("00011", '-d'),
         "PST": ("00100", '-d'), "PLD": ("00101", '-d'),
         "CND": ("00110", '-c'), "LIM": ("00111", '-r'),
         "RST": ("01000", '-r'), "AST": ("01001", '-r'),
         "INC": ("01010", '-r'), "RSH": ("01011", '-r'),
         "ADD": ("01100", '-r'), "SUB": ("01101", '-r'),
         "XOR": ("01110", '-r'), "POI": ("01111", '-r'),
         "NOP": ("100", '-n'), "JMP": ("101", '-l'),
         "MST": ("110", '-a'), "MLD": ("111", '-a')}

    def contains(self, mnemonic):
        return bool(mnemonic in self.code_table)

    def code(self, mnemonic):
        return self.code_table[mnemonic]
