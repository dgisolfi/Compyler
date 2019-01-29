
#!/usr/bin/python3
from setuptools import setup

setup(
    name='Compyler',
    version='0.0.1',
    description='Compiler for Spring 2019 Compilers Course, implemented in python.'+ 
    'Compiles a custom language into a subset of the 6502 opcodes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dgisolfi/Compyler',
    author='dgisolfi',
    license='MIT',
    packages=['src'],
    install_requires=['termcolor>=1.1.0','tqdm>=4.28.1'],
    zip_safe=False
)