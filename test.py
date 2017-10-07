#!/usr/bin/env python3

# tests

from lexer import lexer


def test_lexer():
    '''test lexer'''
    data = '''
    LDR R1, =3
    MOV R1, R2
    ADD R1, R2, R3
    SUB R1, R2, R3
    MUL R1, R2, R3
    '''
    lexer.input(data)

    for token in lexer:
        print(token)


if __name__ == '__main__':
    # do things
    test_lexer()
