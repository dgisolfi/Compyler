# Compyler [![Compyler version](https://img.shields.io/pypi/v/Compyler.svg)](https://pypi.org/project/Compyler)
Compiler for Spring 2019 Compilers Course, implemented in python. Compiles a custom language into a subset of the 6502 opcodes.  

## Setup
To run the Compyler it must be installed. It can be installed either from pypi or from the source code of the directory.

### From PyPi

Simply use pip to install the [latest release](https://pypi.org/project/Compyler/) of the compyler. To do so run `pip install Compyler`. 

### From Source

Either in a Python Virtual Environment or just on your machine in the root of the directory run `make install` this will install the compyler from the source code in the repo using the setup.py file. If you would like to uninstall simply run `make uninstall`

## Compiling

Once setup has been completed an Alan++ source code file can be compiled. To do so run `compyler /path/to/file`

#### Arguements

**path** - The path of an Alan++ source file to be compiled.

#### Flags

**--verbose or -v** - when passed all actions of compiler will be logged to stdout.

**--prettytree or -p** - Outputs CST and AST in a fancier form.

#### Example

`compyler -v -p ./examples/AssignVals.txt`

## Releases

0.1.0 - [Project1](https://github.com/dgisolfi/Compyler/tree/Project1)

0.2.0 - [Project2](https://github.com/dgisolfi/Compyler/tree/Project2)

0.3.2 - [Project3](https://github.com/dgisolfi/Compyler/tree/Project3)

0.4.0 - [Project4](https://github.com/dgisolfi/Compyler/tree/Project4)

## Developing

To develop the compyler it would be a nuisance to install each time a change is made, to avoid this use a python virtual environment. To create a Virtual environment or venv use the following command `python3 -m venv/path/to/new/virtual/environment` The path should be pointed at this repository. To enter a venv that already exists navigate to the bin dir inside of env and run `source activate`. In the case of this repo the command would look like this, `source ./env/bin/activate`.

Once in a venv to run the compyler without installing use the following format: `python3 compyler /path/to/source/file` while in the root of the directory.

## Publishing to PyPi

To publish the latest release of the build to pypi run the following recipe: `make release`. This will test, build and publish the release to pypi.
