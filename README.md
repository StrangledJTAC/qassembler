# qassembler

A hopefully improved version of @Qsmally's [QCPU-Assembler](https://github.com/QSmally/QCPU-Assembler). Implemented in Python.

## Features

* Label Support: You may now define labels and use them in JMP instructions.
* Error Reporting: qassembler will now halt and report programmer errors.

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
qas.py -f ~\files\test.s
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
