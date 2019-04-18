#!/usr/bin/python3
# 2019-1-30
# Daniel Nicolas Gisolfi

lexemes = {
    'TYPE': {
        'priority': 0,
        'pattern': r'^(int|string|boolean)$',
    },
    'BOOLEAN': {
        'priority': 0,
        'pattern':r'^(true|false)$',
    },
    'BOOL_OP':{
        'priority': 2,
        'pattern':r'^(!=|==)$',
    },
    'ADDITION_OP': {
        'priority': 2,
        'pattern': r'^\+$'
    },
    'WHILE': {
        'priority': 0,
        'pattern': r'^while$'
    },
    'PRINT': {
        'priority': 0,
        'pattern': r'^print$'
    },
    'ASSIGN_OP': {
        'priority': 2,
        'pattern': r'^=$'
    },
    'LEFT_PAREN': {
        'priority': 2,
        'pattern': r'^\($'
    },
    'RIGHT_PAREN': {
        'priority': 2,
        'pattern': r'^\)$'
    },
    'LEFT_BRACE': {
        'priority': 2,
        'pattern': r'^{$'
    },
    'RIGHT_BRACE': {
        'priority': 2,
        'pattern': r'^}$'
    },
    'DIGIT': {
        'priority': 3,
        'pattern': r'^\d$'
    },
    'CHAR': {
        'priority': 4,
        'pattern': r'^[a-z]{1}$'
    },
    'QUOTE': {
        'priority': 2,
        'pattern': r'^"$'
    },
    'ID': {
        'priority': 1,
        'pattern': r'^[a-z]$'
    },
    'EOP': {
        'priority': 2,
        'pattern': r'^\$$'
    },
    'IF': {
        'priority': 0,
        'pattern': r'^if$'
    }
}

# Lexemes that will occur in the buffer rather than as a single char.
# They are sorted by length in descending order and seperate from 
# the default lexeme list for effiecincy
buffer_lexemes = {
    'ID': {
        'pattern': r'^[a-z]',
        'token': 'ID'
    },
    'DIGIT': {
        'pattern': r'^\d',
        'token': 'DIGIT'
    },
    'IF': {
        'pattern': r'^if',
        'token': 'IF',
        'value': 'if'
    },
    'INT': {
        'pattern': r'^int',
        'token': 'TYPE',
        'value': 'int'
    },
    'TRUE': {
        'pattern': r'^true',
        'token': 'BOOLEAN',
        'value': 'true'
    },
    'FALSE': {
        'pattern': r'^false',
        'token': 'BOOLEAN',
        'value': 'false'
    },
    'STRING': {
        'pattern': r'^string',
        'token': 'TYPE',
        'value': 'string'
    },
    'WHILE': {
        'pattern': r'^while',
        'token': 'WHILE',
        'value': 'while'
    },
    'PRINT': {
        'pattern': r'^print',
        'token': 'PRINT',
        'value': 'print'
    },
    'BOOLEAN': {
        'pattern': r'^boolean',
        'token': 'TYPE',
        'value': 'boolean'
    }
}