
#!/usr/bin/python3
from setuptools import setup

setup(
    name='Compyler',
    version='0.3.2',
    description='Compiler for Spring 2019 Compilers Course, implemented in python.'+ 
    'Compiles a custom language into a subset of the 6502 opcodes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dgisolfi/Compyler',
    author='dgisolfi',
    license='MIT',
    packages=['compyler'],
    install_requires=[
        'termcolor>=1.1.0',
        'click>=7.0',
        'treelib>=1.5.3', 
        'beautifultable>=0.7.0'
    ],
    zip_safe=False,
    entry_points='''
    [console_scripts]
    compyler=compyler.__main__:main
    '''
)