#!/usr/bin/env python3

# tokenise the program
# uses: ply

# handles following instructions -
# LDR RX, =N
# MOV RX, RY
# ADD RX, RY, RZ
# SUB RX, RY, RZ
# MUL RX, RY, RZ

import ply.lex as lex

# tokens
tokens = (
    'INSTRUCTION',
    'REGISTER',
    'NUMBER',
    'COMMENT',
    'COMMA',
)


def t_INSTRUCTION(t):
    r'(LDR|MOV|ADD|SUB|MUL) '
    t.value = t.value.strip()
    return t


def t_REGISTER(t):
    r'R\d{1}'
    return t


def t_NUMBER(t):
    r'=\d+'
    t.value = int(t.value[1:])
    return t


def t_COMMENT(t):
    r';.*$'
    return t


def t_COMMA(t):
    r','
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    t.lexer.skip(1)


t_ignore = ' \t'


lexer = lex.lex()
