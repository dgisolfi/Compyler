#!/usr/bin/python3
# 2019-1-30

lexemes = {
    'TYPE': {
        'priority': 0,
        'pattern': r'^(int|string|boolean)$',
    },
    'BOOLEAN': {
        'priority': 0,
        'pattern':r'^(true|false)$',
    },
    'INEQUALITY_OP':{
        'priority': 2,
        'pattern':r'^!=$',
    },
    'EQUALITY_OP':{
        'priority': 2,
        'pattern': r'^==$'
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
    'L_PAREN': {
        'priority': 2,
        'pattern': r'^\($'
    },
    'R_PAREN': {
        'priority': 2,
        'pattern': r'^\)$'
    },
    'L_BRACE': {
        'priority': 2,
        'pattern': r'^{$'
    },
    'R_BRACE': {
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
