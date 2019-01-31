#!/usr/bin/python3
# 2019-1-30

lexemes = {
    'TYPE': r'^(int|string|boolean)$',
    'BOOLEAN': r'^(true|false)$',
    'INEQUALITY_OP': r'^!=$',
    'EQUALITY_OP': r'^==$',
    'ADDITION_OP': r'^\+$',
    'WHILE':  r'^while$',
    'PRINT': r'^print$',
    'ASSIGN_OP': r'^=$',
    'L_PAREN': r'^\($',
    'R_PAREN': r'^\)$',
    'L_BRACE': r'^{$',
    'R_BRACE': r'^}$',
    'DIGIT': r'^\d$',
    'ID': r'^[a-z]$',
    'CHAR': r'[a-z]',
    'QUOTE': r'^"$',
    'EOP': r'^\$$',
    'IF': r'^if$'
}