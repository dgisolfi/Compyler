# Compiler
Compiler for Spring 2019 Compilers Course, implemented in python. Compiles a custom language into a subset of the 6502 opcodes.  

## Setup
Running the shell for the compiler can be done in one of two ways:

### Running from the source code

1. Run `make init` in the root of the repository(this will install all requirements)
2. Run `python3 ./src/cli/shell.py` from the root of the repository

### Creating or using the latest build

1. Run `make install` to build and install the compiler and shell to use it.
2. Run `python3 -m compiler`

## Compiling

Once in an instance of the shell for the compiler, run `compile <file>` providing a file path to compile. For example programs use any of the available ones located in the examples directory in the root of the repo. EX: `compile ./examples/AlansTestCase.txt`

## Testing

To run tests for the compiler run the command `make test` in the root of the directory. This should be done before releasing a new version to avoid breaking previous functionality.

## Publishing to PyPi

To publish the latest release of the build to pypi run the following recipe: `make release`. This will test, build and publish the release to pypi.



