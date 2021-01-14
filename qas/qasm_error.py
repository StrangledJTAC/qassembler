class AssemblerError(Exception):
    def __init__(self, reason):
        self.reason = reason


class AssemblerParseError(AssemblerError):
    def __init__(self, line, reason):
        super().__init__(reason)
        self.line = line


class AssemblerMemoryError(AssemblerError):
    def __str__(self):
        return f"QCPU instruction memory limit exceeded: {self.reason}"


class AssemblerSyntaxError(AssemblerParseError):
    def __str__(self):
        return f"Syntax error on line {self.line}: {self.reason}"


class AssemblerRangeError(AssemblerParseError):
    def __str__(self):
        return f"Range error on line {self.line}: {self.reason}"


class AssemblerTypeError(AssemblerParseError):
    def __str__(self):
        return f"Type error on line {self.line}: {self.reason}"


class AssemblerInternalError(AssemblerParseError):
    def __str__(self):
        return f"Internal error on line {self.line}: {self.reason}"
