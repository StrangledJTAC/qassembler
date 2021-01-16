import re
import qasm_error as asm_err
import sys


class Parser:
    def __init__(self, infile, symbolizer, generator):
        self.source = self.preprocessor(infile)
        self.current_command = ""
        self.lindex = 0
        self.symbolizer = symbolizer
        self.generator = generator
        self.__opcode = ""
        self.__operandtype = ""

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
        return not bool(self.lindex == len(self.source))

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
        if len(self.source) > 32:  # test program size within bounds
            raise asm_err.AssemblerMemoryError("Program Size Maximum 32 bytes")

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
        if not self.symbolizer.contains(label.group()):
            self.symbolizer.addEntry(label.group(), self.lindex - 1)
        else:
            ldef_reason = "Label defined more than once"
            raise asm_err.AssemblerSyntaxError(self.lindex, ldef_reason)

    def operation(self):
        opcode = re.match(r"[A-Z]{3}", self.current_command)
        if opcode is None:
            m_reason = "Malformed Instruction"
            raise asm_err.AssemblerSyntaxError(self.lindex, m_reason)
        if not self.generator.contains(opcode.group()):
            u_reason = "Unrecognized Instruction."
            raise asm_err.AssemblerSyntaxError(self.lindex, u_reason)
        else:
            self.__opcode = opcode.group()
            operation_type = self.generator.code(self.__opcode)
            self.__operandtype = operation_type[1]

            operation = operation_type[0] + self.operand()
            return operation

    def operand(self):
        """

        Parameters
        ----------
        agree : str
            identifier for acceptable operands for given opcode.

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

        if self.__operandtype == '-r':
            register = re.search(r"(?<=\s)\$\d", self.current_command)
            if register is not None:
                register = register.group()
                num = int(re.search(r"\d", register).group())
                if num in range(8):
                    return self.symbolizer.getAddress(register)
                else:
                    v_reason = "Register out of Range: $0 - $7"
                    raise asm_err.AssemblerRangeError(self.lindex, v_reason)
            else:
                r_reason = "Expected Operand Type: Register"
                raise asm_err.AssemblerTypeError(self.lindex, r_reason)

        elif self.__operandtype == '-a':
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

        elif self.__operandtype == '-l':
            lpattern = r"(?<=\s)[a-zA-Z\._][a-zA-Z\._0-9]*"
            plabel = re.search(lpattern, self.current_command)
            if plabel is not None:
                if self.symbolizer.contains(plabel.group()) is True:
                    dec_line = self.symbolizer.getAddress(plabel.group())
                    bin_line = "{0:b}".format(dec_line).zfill(5)
                    return bin_line
                else:
                    ld_reason = f"Undefined Label: {plabel.group()}"
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

        elif self.__operandtype == '-c':
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

        elif self.__operandtype == '-d':
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

        elif self.__operandtype == '-n':
            anything = re.search(r"(?<=[A-Z]{3}).+", self.current_command)
            if anything is None:
                if self.__opcode == 'NOP':
                    return '00000'
                else:
                    return '000'
            else:
                n_reason = "Expected Operand Type: None"
                raise asm_err.AssemblerTypeError(self.lindex, n_reason)

        else:
            u_reason = "OPERAND_TYPE_NOT_DEFINED: Please Report this Bug."
            raise asm_err.AssemblerInternalError(self.lindex, u_reason)

