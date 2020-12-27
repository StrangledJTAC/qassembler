# -*- coding: utf-8 -*-

class AssemblerError(Exception):
    pass


class AssemblerSyntaxError(AssemblerError):
    def __init__(self, line, reason):
        self.line = line
        self.reason = reason

    def __str__(self):
        return "Syntax error on line %d: %s" % (self.line, self.reason)


class AssemblerRangeError(AssemblerError):
    def __init__(self, line, reason):
        self.line = line
        self.reason = reason

    def __str__(self):
        return "Range error on line %d: %s" % (self.line, self.reason)
