class symbolizer:
    def __init__(self):
        self.symbol_table = {
         "$0": "000", "$1": "001", "$2": "010", "$3": "011", "$4": "100",
         "$5": "101", "$6": "110", "$7": "111"}

    def addEntry(self, symbol, address):
        self.symbol_table[symbol] = address

    def contains(self, symbol):
        if symbol in self.symbol_table:
            return True
        else:
            return False

    def Getaddress(self, symbol):
        return self.symbol_table[symbol]
