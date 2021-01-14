# qassembler

A hopefully improved version of @Qsmally's [QCPU-Assembler](https://github.com/QSmally/QCPU-Assembler). Implemented in Python.

## Features

* Label Support: You may now define labels and use them in JMP instructions. Valid label definitions must begin with an identifier and end with a colon(:). 
An identifier is an sequence of alphanumeric, underscore(\_), or dot(.) characters of arbitrary length, although the first character must be a letter, the underscore character(\_) or dot(.). Labels are case sensitive.
* Error Reporting: qassembler will now halt and report programmer errors.
* Comment Support (inherited from QCPU-Assembler): All characters following the semicolon(;) or slash(/) characters, inclusive, are excluded from analysis by the assembler.

## Limitations

* Variables remain unsupported as the targetted hardware does not implement the necessary memory protection techniques.
* Due to unclear ISA specification, the current implementation does not allow operands for the MSC opcode.

## Installation

1. Ensure that python3 is installed and on PATH
2. Clone the repository.
3. Navigate to .../qassembler/qas and execute the following shell command:
```
chmod +x qas.py
```

## Usage

### File Mode:
```
qas.py -f filepath

example:
qas.py -f ~/docs/test.s
qas.py -f test.s
```
.txt file containing the assembled machine instructions should appear in the current working directory.

### Test Mode:
1. Place the input test files in .../qassembler/tests
2. Place the expected output files in .../qassembler/output/expected
```
qas.py -t 
```
## Contributing

Priority: The author does not have access to the target hardware and thus cannot generate schematics. Please work on this if possible.
