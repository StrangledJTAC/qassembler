#! /usr/bin/python3

import argparse
import filecmp
import pathlib
import qasm_parser
import qasm_code


class Assembler:
    def __init__(self, infile):
        self.__assembled_list = []
        self.__infile = infile

    def assemble(self):
        # First Pass: Collect all labels and add them to symbol table
        symbolizer = qasm_code.Symbolizer()  # initialize symbolizer object
        generator = qasm_code.Generator()  # initialize code generator object
        parser = qasm_parser.Parser(self.__infile, symbolizer, generator)

        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType() == 'label':
                parser.label()
            else:
                continue

        # Reset parser and exclude label definitions from further analysis
        parser.reset()

        # Second Pass: Collect instructions and generate machine code
        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType() == 'data':
                self.__assembled_list.append(parser.data())

            elif parser.commandType() == 'operation':
                self.__assembled_list.append(parser.operation())

            else:
                continue

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
    if infile.test:
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
