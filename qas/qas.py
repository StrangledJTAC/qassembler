#! /usr/bin/python3

import argparse
import filecmp
import pathlib
import qasm_parser
import qasm_code
import qsymbol_table
import error_classes as asm_error


def assemble(infile):
    assembled_list = []

    # First Pass: Collect all labels and add them to symbol table
    first = qasm_parser.parser(infile)  # initialize parser object
    symbolizer = qsymbol_table.symbolizer()  # initialize symbolizer object
    while first.hasMoreCommands():
        first.advance()
        if first.commandType() == 'label':
            if symbolizer.contains(first.label()) is False:
                symbolizer.addEntry(first.label(), first.lindex - 1)
            else:
                ldef_reason = "Label defined more than once"
                raise asm_error.AssemblerSyntaxError(first.lindex, ldef_reason)
        else:
            continue

    # Reset parser and exclude label definitions from further analysis
    first.reset()
    if len(first.source) > 32:
        raise asm_error.AssemblerMemoryError("Program Size Maximum 32 bytes")

    # Second Pass: Collect instructions and generate machine code
    generator = qasm_code.generator()  # initialize code generator object
    while first.hasMoreCommands():
        first.advance()
        if first.commandType() == 'data':
            assembled_list.append(first.data())
        elif first.commandType() == 'operation':
            opcode = generator.code(first.operation())
            operation = opcode[0] + first.operand(opcode[1], symbolizer)
            assembled_list.append(operation)
        else:
            ctype_reason = ("UNDEFINED_COMMAND_TYPE: Please Report this Bug")
            raise asm_error.AssemblerInternalError(first.lindex, ctype_reason)

    return assembled_list


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f", action="store", required=False)
    parser.add_argument("--test", "-t", action="store_true", default=False)
    infile = parser.parse_args()
    if not (infile.file or infile.test):
        parser.error("qas fatal error: No action requested. Use -f or -t.")

    # test mode > do not invoke in normal operations (overrides other modes)
    if infile.test is True:
        pardir = pathlib.Path(__file__).parent.absolute().parent
        testdir = pardir.joinpath("tests")
        for file in testdir.iterdir():
            print(f"Testing {file}")
            assembled_test = assemble(file)

            inpath = pathlib.PurePath(file)
            outfile_name = inpath.name.split('.')[0] + '.txt'
            asm_dir = pathlib.Path(__file__).parent.absolute().parent
            output_path = asm_dir.joinpath('output', outfile_name)

            with open(output_path, 'w') as outfile:
                outfile.write("\n".join(str(item) for item in assembled_test))
        # generate test report
        outputdir = asm_dir.joinpath("output")
        comp = filecmp.dircmp(outputdir, outputdir.joinpath("expected"))
        comp.report()

    else:  # file mode
        assembled_file = assemble(infile.file)

        inpath = pathlib.PurePath(infile.file)
        outfile_name = inpath.name.split('.')[0] + '.txt'
        asm_dir = pathlib.Path.cwd()
        output_path = asm_dir.joinpath(outfile_name)

        with open(output_path, 'w') as outfile:
            outfile.write("\n".join(str(item) for item in assembled_file))


main()
