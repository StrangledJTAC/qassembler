class AssemblerError(Exception):
    pass


class AssemblerSyntaxError(AssemblerError):
    def __init__(self, line, reason):
        self.line = line
        self.reason = reason

    def __str__(self):
        return f"Syntax error on line {self.line}: {self.reason}"


class AssemblerRangeError(AssemblerError):
    def __init__(self, line, reason):
        self.line = line
        self.reason = reason

    def __str__(self):
        return f"Range error on line {self.line}: {self.reason}"


class AssemblerMemoryError(AssemblerError):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f"QCPU instruction memory limit exceeded: {self.reason}"


class AssemblerTypeError(AssemblerError):
    def __init__(self, line, reason):
        self.line = line
        self.reason = reason

    def __str__(self):
        return f"Type error on line {self.line}: {self.reason}"


class AssemblerInternalError(AssemblerError):
    def __init__(self, line, reason):
        self.line = line
        self.reason = reason

    def __str__(self):
        return f"Internal error on line {self.line}: {self.reason}"
