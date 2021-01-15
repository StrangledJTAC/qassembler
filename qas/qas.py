#! /usr/bin/python3

import argparse
import filecmp
import pathlib
import qasm_parser
import qasm_code
import qasm_error as asm_err


class Assembler:
    def __init__(self, infile):
        self.__assembled_list = []
        self.__infile = infile

    def assemble(self):
        # First Pass: Collect all labels and add them to symbol table
        first = qasm_parser.Parser(self.__infile)  # initialize parser object
        symbolizer = qasm_code.Symbolizer()  # initialize symbolizer object
        while first.hasMoreCommands():
            first.advance()
            if first.commandType() == 'label':
                if symbolizer.contains(first.label()) is False:
                    symbolizer.addEntry(first.label(), first.lindex - 1)
                else:
                    ldef_reason = "Label defined more than once"
                    raise asm_err.AssemblerSyntaxError(first.lindex, ldef_reason)
            else:
                continue

        # Reset parser and exclude label definitions from further analysis
        first.reset()
        if len(first.source) > 32:  # test program size within bounds
            raise asm_err.AssemblerMemoryError("Program Size Maximum 32 bytes")

        # Second Pass: Collect instructions and generate machine code
        generator = qasm_code.Generator()  # initialize code generator object
        while first.hasMoreCommands():
            first.advance()
            if first.commandType() == 'data':
                self.__assembled_list.append(first.data())
            elif first.commandType() == 'operation':
                if generator.contains(first.operation()):
                    opcode = generator.code(first.operation())
                    operation = opcode[0] + first.operand(opcode[1], symbolizer)
                    self.__assembled_list.append(operation)
                else:
                    u_reason = "Unrecognized Instruction."
                    raise asm_err.AssemblerSyntaxError(first.lindex, u_reason)
            else:
                ctype_reason = "UNDEFINED_COMMAND_TYPE: Please Report this Bug"
                raise asm_err.AssemblerInternalError(first.lindex, ctype_reason)

        return self.__assembled_list


if __name__ == '__main__':

    ASM_DIR = pathlib.Path(__file__).parent.absolute().parent  # repo main dir
    TEST_DIR = ASM_DIR.joinpath("tests")  # test input dir
    OUTPUT_DIR = ASM_DIR.joinpath("output")  # test output dir
    EXPECTED_DIR = OUTPUT_DIR.joinpath("expected")  # test expected ouput dir
    CWD = pathlib.Path.cwd()  # current working dir

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", action="store", required=False)
    parser.add_argument("--test", "-t", action="store_true", default=False)
    infile = parser.parse_args()

    if not (infile.file or infile.test):
        parser.error("qas fatal error: No action requested. Use -f or -t.")

    # test mode > do not invoke in normal operations (overrides other modes)
    if infile.test is True:
        for file in TEST_DIR.iterdir():
            print(f"Testing {file}")
            assembled_test = Assembler(file).assemble()

            inpath = pathlib.PurePath(file)
            outfile_name = inpath.stem + '.txt'
            output_path = OUTPUT_DIR.joinpath(outfile_name)

            with open(output_path, 'w') as outfile:
                outfile.write("\n".join(str(item) for item in assembled_test))
        # generate test report
        comp = filecmp.dircmp(OUTPUT_DIR, EXPECTED_DIR)
        print(''), comp.report()

    else:  # file mode
        assembled_file = Assembler(infile.file).assemble()

        inpath = pathlib.PurePath(infile.file)
        outfile_name = inpath.stem + '.txt'
        output_path = CWD.joinpath(outfile_name)

        with open(output_path, 'w') as outfile:
            outfile.write("\n".join(str(item) for item in assembled_file))
