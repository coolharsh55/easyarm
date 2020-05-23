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
registers = dict((r, 0) for r in range(1, NO_REGISTERS + 1))
STACK = []
TABS = 0
BYTES = {}

import ply.lex as lex
from colorama import init
init()
from colorama import Fore, Back, Style

# tokens
tokens = (
    'INSTRUCTION_LDR',
    'INSTRUCTION_MOV',
    'INSTRUCTION_ADD',
    'INSTRUCTION_SUB',
    'INSTRUCTION_MUL',
    'INSTRUCTION_LDRB',
    'INSTRUCTION_CMP',
    'INSTRUCTION_BEQ',
    'INSTRUCTION_B',
    'INSTRUCTION_BLT',
    'INSTRUCTION_DCB',
    'INSTRUCTION_DCD',
    'INSTRUCTION_SPACE',
    'REGISTER',
    'REGISTER_ADDR',
    'NUMBER',
    'COMMENT',
    'LABEL',
    'LABEL_REF',
)


def t_INSTRUCTION_LDRB(t):
    r'LDRB '
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


def t_INSTRUCTION_LDR(t):
    r'LDR '
    t.value = t.value.strip()
    return t


def t_INSTRUCTION_CMP(t):
    r'CMP '
    t.value = t.value.strip()
    return t


def t_INSTRUCTION_BEQ(t):
    r'BEQ '
    t.value = t.value.strip()
    return t


def t_INSTRUCTION_BLT(t):
    r'BLT '
    t.value = t.value.strip()
    return t


def t_INSTRUCTION_B(t):
    r'[bB] '
    t.value = t.value.strip()
    return t


def t_INSTRUCTION_DCB(t):
    r'DCB\s+.+'
    t.value = t.value[4:].strip()
    return t


def t_INSTRUCTION_DCD(t):
    r'DCD\s+.+'
    t.value = t.value[4:].strip()
    return t


def t_INSTRUCTION_SPACE(t):
    r'SPACE\s+\d+'
    t.value = int(t.value[5:].strip())
    return t


def t_REGISTER(t):
    r'R\d{1}'
    t.value = int(t.value[1:])
    return t


def t_REGISTER_ADDR(t):
    r'\[R\d{1}\]'
    t.value = t.value[2:-1]
    return t


def t_NUMBER(t):
    r'[=#]{1}\d+'
    t.value = int(t.value[1:])
    return t


def t_COMMENT(t):
    r';.+'
    t.value = t.value[1:]
    return t


def t_LABEL(t):
    r'\w+'
    return t


def t_LABEL_REF(t):
    r'=\w+'
    t.value = t.value[1:]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    t.lexer.skip(1)


t_ignore = ' \t,'
lexer = lex.lex()

import ply.yacc as yacc

def _tabs(value=0):
    global TABS
    if value:
        TABS += value
        if TABS < 0:
            TABS = 0
    return '\t' * TABS


def p_expression(p):
    'expression : expression COMMENT'
    print(_tabs(), Fore.CYAN, '#', p[2], Style.RESET_ALL)


def p_label(p):
    'expression : LABEL'
    style = Fore.RED
    if p[1] == 'while' or p[1].startswith('while'):
        print(_tabs(), style, p[1], Style.RESET_ALL)
        _tabs(1)
    elif p[1] in ('endwhile', 'endwh'):
        _tabs(-1)
        print(_tabs(), style, p[1], Style.RESET_ALL)
    elif p[1].startswith('end'):
        _tabs(-1)
        print(_tabs(), style, p[1], Style.RESET_ALL)
    else:
        print(_tabs(), style, p[1], Style.RESET_ALL)


def p_databytes(p):
    '''expression : LABEL INSTRUCTION_DCB
                  | LABEL INSTRUCTION_DCD'''
    BYTES[p[1]] = p[2]
    print(_tabs(), '%s = %s' % (p[1], p[2]))


def p_allocate_space(p):
    'expression : LABEL INSTRUCTION_SPACE'
    BYTES[p[1]] = '%sbytes' % p[2]
    print(_tabs(), '%s = [%s]bytes' % (p[1], p[2]))


def p_load(p):
    'expression : INSTRUCTION_LDR REGISTER NUMBER'
    print(_tabs(), 'R%s = %s' % (p[2], p[3]))


def p_load_addr(p):
    'expression : INSTRUCTION_LDR REGISTER REGISTER_ADDR'
    print(_tabs(), 'R%s = *R%s' % (p[2], p[3]))


def p_loadbyte(p):
    'expression : INSTRUCTION_LDRB REGISTER REGISTER_ADDR'
    print(_tabs(), 'R%s = *R%s' % (p[2], p[3]))


def p_loadstring(p):
    'expression : INSTRUCTION_LDR REGISTER LABEL_REF'
    print(_tabs(), 'R%s = addr(%s)' % (p[2], p[3]))


def p_mov(p):
    '''expression : INSTRUCTION_MOV REGISTER REGISTER
                  | INSTRUCTION_MOV REGISTER NUMBER'''
    print(_tabs(), 'R%s = %s' % (p[2], p[3]))


def p_compare(p):
    '''expression : INSTRUCTION_CMP REGISTER NUMBER
                  | INSTRUCTION_CMP REGISTER REGISTER'''
    STACK.append((p[2], p[3]))


def p_branch(p):
    'expression : INSTRUCTION_B LABEL'
    print(_tabs(), 'goto %s' % p[2])


def p_branch_equal(p):
    '''expression : INSTRUCTION_BEQ LABEL
                  | INSTRUCTION_BLT LABEL'''
    registers = STACK.pop()
    if p[1] == 'BEQ':
        print(_tabs(), 'if R%s == %s' % registers)
    elif p[1] == 'BLT':
        print(_tabs(), 'if R%s < %s' % registers)
    print(_tabs(), '\tgoto %s' % p[2])


def p_mads(p):
    '''expression : INSTRUCTION_ADD REGISTER REGISTER REGISTER
                  | INSTRUCTION_SUB REGISTER REGISTER REGISTER
                  | INSTRUCTION_MUL REGISTER REGISTER REGISTER'''
    if p[1] == 'ADD':
        sign = '+'
    elif p[1] == 'SUB':
        sign = '-'
    elif p[1] == 'MUL':
        sign = '*'
    if p[2] == p[3]:
        print(_tabs(), 'R%s %s= R%s' % (p[2], sign, p[4]))
    else:
        print(_tabs(), 'R%s = R%s %s R%s' % (p[2], p[3], sign, p[4]))


def p_mads_value(p):
    '''expression : INSTRUCTION_ADD REGISTER REGISTER NUMBER
                  | INSTRUCTION_SUB REGISTER REGISTER NUMBER
                  | INSTRUCTION_MUL REGISTER REGISTER NUMBER'''
    if p[1] == 'ADD':
        sign = '+'
    elif p[1] == 'SUB':
        sign = '-'
    elif p[1] == 'MUL':
        sign = '*'
    if p[2] == p[3]:
        print(_tabs(), 'R%s %s= %s' % (p[2], sign, p[4]))
    else:
        print(_tabs(), 'R%s = R%s %s %s' % (p[2], p[3], sign, p[4]))


def p_error(p):
    pass


parser = yacc.yacc()
