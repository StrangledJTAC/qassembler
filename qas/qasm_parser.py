import re
import error_classes as asm_err
import sys


class Parser:
    def __init__(self, infile):
        self.source = self.preprocessor(infile)
        self.current_command = ""
        self.lindex = 0

    def preprocessor(self, infile):
        try:
            with open(infile, 'r') as asm:
                lines = asm.readlines()
        except FileNotFoundError:
            sys.exit("qas fatal error: File does not exist.")

        # strip comments, remove empty lines, and unnecessary whitespace
        lines = [re.sub(r"[;/].*", "", line) for line in lines]
        lines = [line for line in lines if line != ""]
        lines = [line.strip() for line in lines]
        return lines

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
            else:
                continue

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
            v_reason = "Value out of range: 0 - 255"
            raise asm_err.AssemblerRangeError(self.lindex, v_reason)

    def label(self):
        label = re.match(r"[a-zA-Z\._][a-zA-Z\._0-9]*(?=:)", self.current_command)
        return label.group()

    def operation(self):
        opcode = re.match(r"[A-Z]{3}", self.current_command).group()
        return opcode

    def operand(self, agree, symbolizer):
        """

        Parameters
        ----------
        agree : str
            identifier for acceptable operands for given opcode.
        symbolizer : object
            symbolizer instance handed from assemble().

        Raises
        ------
        asm_err.AssemblerTypeError
            if opcode and operands do not agree.

        asm_err.AssemblerRangeError
            if operand values out of bounds.

        asm_err.AssemblerSyntaxError
            if parser finds undefined label as operand

        asm_err.AssemblerUnknownError
            if 'agree' parameter is undefined.

        Returns
        -------
        operands : str
            Assembly operands in machine-instruction form.

        """
        ipattern = r"(?<=\s)\d+"

        if agree == '-r':
            register = re.search(r"(?<=\s)\$\d", self.current_command)
            if register is not None:
                register = register.group()
                num = int(re.search(r"\d", register).group())
                if num in range(8):
                    return symbolizer.Getaddress(register)
                else:
                    v_reason = "Register out of Range: $0 - $7"
                    raise asm_err.AssemblerRangeError(self.lindex, v_reason)
            else:
                r_reason = "Expected Operand Type: Register"
                raise asm_err.AssemblerTypeError(self.lindex, r_reason)

        elif agree == '-a':
            address = re.search(ipattern, self.current_command)
            if address is not None:
                address = int(address.group())
                if address in range(32):
                    return "{0:b}".format(address).zfill(5)
                else:
                    v_reason = "Address out of range: 0 - 31"
                    raise asm_err.AssemblerRangeError(self.lindex, v_reason)
            else:
                a_reason = "Expected Operand Type: Address"
                raise asm_err.AssemblerTypeError(self.lindex, a_reason)

        elif agree == '-l':
            lpattern = r"(?<=\s)[a-zA-Z\._][a-zA-Z\._0-9]*"
            plabel = re.search(lpattern, self.current_command)
            if plabel is not None:
                if symbolizer.contains(plabel.group()) is True:
                    dec_line = symbolizer.Getaddress(plabel.group())
                    bin_line = "{0:b}".format(dec_line).zfill(5)
                    return bin_line
                else:
                    ld_reason = f"Undefined Label{plabel.group()}"
                    raise asm_err.AssemblerSyntaxError(self.lindex, ld_reason)
            else:
                address = re.search(ipattern, self.current_command)
                if address is not None:
                    address = int(address.group())
                    if address in range(32):
                        return "{0:b}".format(address).zfill(5)
                    else:
                        v_reason = "Address out of range: 0 - 31"
                        raise asm_err.AssemblerRangeError(self.lindex, v_reason)
                else:
                    l_reason = "Expected Operand Type: Label/Address"
                    raise asm_err.AssemblerTypeError(self.lindex, l_reason)

        elif agree == '-c':
            cond = re.search(ipattern, self.current_command)
            if cond is not None:
                cond = int(cond.group())
                if cond in (0, 1, 2, 4):
                    return "{0:b}".format(cond).zfill(3)
                else:
                    v_reason = "Condition out of range: 0 - 2 OR 4"
                    raise asm_err.AssemblerRangeError(self.lindex, v_reason)
            else:
                c_reason = "Expected Operand Type: Condition"
                raise asm_err.AssemblerTypeError(self.lindex, c_reason)

        elif agree == '-d':
            device = re.search(ipattern, self.current_command)
            if device is not None:
                device = int(device.group())
                if device in range(8):
                    return "{0:b}".format(device).zfill(3)
                else:
                    v_reason = "Port/Storage Number out of range: 0 - 7"
                    raise asm_err.AssemblerRangeError(self.lindex, v_reason)
            else:
                d_reason = "Expected Operand Type: Port/Storage Number"
                raise asm_err.AssemblerTypeError(self.lindex, d_reason)

        elif agree == '-n':
            anything = re.search(r"(?<=[A-Z]{3}).+", self.current_command)
            if anything is None:
                if self.operation() == 'NOP':
                    return '00000'
                else:
                    return '000'
            else:
                n_reason = "Expected Operand Type: None"
                raise asm_err.AssemblerTypeError(self.lindex, n_reason)

        else:
            u_reason = "OPERAND_TYPE_NOT_DEFINED: Please Report this Bug."
            raise asm_err.AssemblerUnknownError(self.lindex, u_reason)

