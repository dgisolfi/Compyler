# Compyler
Compiler for Spring 2019 Compilers Course, implemented in python. Compiles a custom language into a subset of the 6502 opcodes.  

## Setup
To run the Compyler its dependencies must be installed. Either in a Python Virtual Environment or just on your machine in the root of the directory run `make init`. This will install all the necessary requirements.

## Compiling

Once setup has been completed an Alan++ source code file can be compiled. To do so run `python3 compyler /path/to/file`

### Arguements

**path** - The path of an Alan++ source file to be compiled.

### Flags

**--verbose || -v** - when passed all logs of actions the compiler is taking will be sent to stout.

#### Example

`python3 compyler -v ./examples/Blocks.txt`

## Testing

To run tests for the compiler run the command `make test` in the root of the directory. This should be done before releasing a new version to avoid breaking previous functionality.

## Publishing to PyPi

To publish the latest release of the build to pypi run the following recipe: `make release`. This will test, build and publish the release to pypi.
