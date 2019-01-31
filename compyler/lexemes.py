#!/usr/bin/python3
# 2019-1-30

lexemes = {
    'TYPE': {
        'priority': 1,
        'pattern': r'^(int|string|boolean)$',

    },
    'BOOLEAN': {
        'priority': 1,
        'pattern':r'^(true|false)$',
    },
    'INEQUALITY_OP':{
        'priority': 1,
        'pattern':r'^!=$',
    },
    'EQUALITY_OP':{
        'priority': 1,
        'pattern': r'^==$'
    },
    'ADDITION_OP': {
        'priority': 1,
        'pattern': r'^\+$'
    },
    'WHILE': {
        'priority': 1,
        'pattern': r'^while$'
    },
    'PRINT': {
        'priority': 1,
        'pattern': r'^print$'
    },
    'ASSIGN_OP': {
        'priority': 1,
        'pattern': r'^=$'
    },
    'L_PAREN': {
        'priority': 1,
        'pattern': r'^\($'
    },
    'R_PAREN': {
        'priority': 1,
        'pattern': r'^\)$'
    },
    'L_BRACE': {
        'priority': 1,
        'pattern': r'^{$'
    },
    'R_BRACE': {
        'priority': 1,
        'pattern': r'^}$'
    },
    'DIGIT': {
        'priority': 1,
        'pattern': r'^\d$'
    },
    'ID': {
        'priority': 1,
        'pattern': r'^[a-z]$'
    },
    'CHAR': {
        'priority': 1,
        'pattern': r'[a-z]{1}$'
    },
    'QUOTE': {
        'priority': 1,
        'pattern': r'^"$'
    },
    'EOP': {
        'priority': 1,
        'pattern': r'^\$$'
    },
    'IF': {
        'priority': 1,
        'pattern': r'^if$'
    }
}
