#!/usr/bin/env python3

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('needs filename')
        sys.exit()
    filename = sys.argv[1]
    with open(filename, 'r') as fd:
        lines = fd.readlines()
        lines = [l.strip() for l in lines]
        lines = [l for l in lines if l]
        while lines and lines[0].lower() != 'start':
            lines.pop(0)
        if not lines:
            print('nothing to process')
            sys.exit()
    from sleeve import parser
    for line in lines:
        # print('>>> ', line)
        parser.parse(line)
