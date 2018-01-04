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
        ''',
    'stringlength': '''
        start
            LDR R1, =str1
            LDR R2, =0 
            LDRB R3, [R1] 
        while 
            CMP R3, #0
            BEQ endwhile
            ADD R1, R1, #1
            LDRB R3, [R1] 
            ADD R2, R2, #1
            B while 
        endwhile 
        stop    B   stop
        AREA    TestData, DATA, READWRITE
        str1    DCB "Friday",0
        END''',
}


def test_parser():
    '''test parser'''
    for line in data['stringlength'].splitlines():
        line = line.strip()
        # print('>>', line)
        parser.parse(line)


if __name__ == '__main__':
    # do things
    test_parser()
