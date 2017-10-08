#!/usr/bin/env python3

# tests

from sleeve import parser
from sleeve import registers


data = {
    'simple': '''
        LDR R1, =3  ; some vanity comment
        MOV R3, R1
        ADD R1, R2, R3 ; more comments
        SUB R1, R2, R3
        ; comment between lines
        ; for testing purposes
        MUL R1, R2, R3
        '''
}


def test_parser():
    '''test parser'''
    for line in data['simple'].splitlines():
        print(line)
        parser.parse(line)
        print(registers)


if __name__ == '__main__':
    # do things
    test_parser()
