#!/usr/bin/env python3

# tokenise the program
# uses: ply

# handles following instructions -
# LDR RX, =N
# MOV RX, RY
# ADD RX, RY, RZ
# SUB RX, RY, RZ
# MUL RX, RY, RZ

NO_REGISTERS = 15
registers = dict((r, 0) for r in range(1, NO_REGISTERS))


import ply.lex as lex

# tokens
tokens = (
    'INSTRUCTION_LDR',
    'INSTRUCTION_MOV',
    'INSTRUCTION_ADD',
    'INSTRUCTION_SUB',
    'INSTRUCTION_MUL',
    'REGISTER',
    'NUMBER',
    'COMMENT',
)


def t_INSTRUCTION_LDR(t):
    r'LDR '
    t.value = t.value.strip()
    return t


def t_INSTRUCTION_MOV(t):
    r'MOV '
    t.value = t.value.strip()
    return t


def t_INSTRUCTION_ADD(t):
    r'ADD '
    t.value = t.value.strip()
    return t


def t_INSTRUCTION_SUB(t):
    r'SUB '
    t.value = t.value.strip()
    return t


def t_INSTRUCTION_MUL(t):
    r'MUL '
    t.value = t.value.strip()
    return t


def t_REGISTER(t):
    r'R\d{1}'
    t.value = int(t.value[1:])
    return t


def t_NUMBER(t):
    r'=\d+'
    t.value = int(t.value[1:])
    return t


def t_COMMENT(t):
    r';.*$'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    t.lexer.skip(1)


t_ignore = ' \t,'
lexer = lex.lex()

import ply.yacc as yacc


def p_expression(p):
    'expression : expression COMMENT'
    pass


def p_load(p):
    'expression : INSTRUCTION_LDR REGISTER NUMBER'
    # print('LOAD', p[2], p[3])
    registers[p[2]] = p[3]
    # print(registers)


def p_mov(p):
    'expression : INSTRUCTION_MOV REGISTER REGISTER'
    # print('MOV', p[2], p[3])
    registers[p[2]] = registers[p[3]]
    # print(registers)


def p_add(p):
    'expression : INSTRUCTION_ADD REGISTER REGISTER REGISTER'
    # print('ADD', p[2], p[3], p[4])
    registers[p[2]] = registers[p[3]] + registers[p[4]]
    # print(registers)


def p_sub(p):
    'expression : INSTRUCTION_SUB REGISTER REGISTER REGISTER'
    # print('SUB', p[2], p[3], p[4])
    registers[p[2]] = registers[p[3]] - registers[p[4]]
    # print(registers)


def p_mul(p):
    'expression : INSTRUCTION_MUL REGISTER REGISTER REGISTER'
    # print('MUL', p[2], p[3], p[4])
    registers[p[2]] = registers[p[3]] * registers[p[4]]
    # print(registers)


def p_error(p):
    pass


parser = yacc.yacc()
