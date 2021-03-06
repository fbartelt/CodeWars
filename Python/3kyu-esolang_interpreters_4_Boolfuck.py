import re

def boolfuck(code, input_=""):
    code = ''.join(cmd for cmd in code if cmd in ['<','[',',',';','+',']','>'])
    if input_:
        input_ = list(''.join('{:08b}'.format(b)[::-1] for b in input_.encode('latin-1')))
    stack, bracket_map = [], {}
    for idx, cmd in enumerate(code):
        if cmd == '[':
            stack.append(idx)
        elif cmd == ']':
            opening = stack.pop()
            bracket_map.update({opening:idx, idx: opening})
    ptr = i = loop = m = 0
    tape, output = ['0'], []
    input_size = len(input_)
    while i < len(code):
        command = code[i]
        if loop:
            if command == '[':
                loop += 1
                if loop == 0: i -= 1
            elif command == ']':
                loop -= 1
        elif command in ['>','<']:
            ptr += (-1)**(command == '<')
            if ptr < 0:
                tape.insert(0,'0')
                ptr = 0
            elif ptr >= len(tape):
                tape.append('0')
        elif command == '+':
            tape[ptr] = '1' if tape[ptr] == '0' else '0'
        elif command == ',':
            tape[ptr] = input_[m] if m<input_size else '0'
            m+=1
        elif command == ';':
            output.append(tape[ptr])
        elif command == '[' and tape[ptr] == '0':
            loop += 1
            i = bracket_map[i]
        elif command == ']':
            loop -=1
            i = bracket_map[i]
        i += 1 if not loop else 0
    ret = bytes(int(b[::-1], 2) for b in re.split('(.{8})', ''.join(output)) if b).decode('latin-1')
    return ret
# HELLO WORLD
#boolfuck(';;;+;+;;+;+;+;+;+;+;;+;;+;;;+;;+;+;;+;;;+;;+;+;;+;+;;;;+;+;;+;;;+;;+;+;+;;;;;;;+;+;;+;;;+;+;;;+;+;;;;+;+;;+;;+;+;;+;;;+;;;+;;+;+;;+;;;+;+;;+;;+;+;+;;;;+;+;;;+;+;+;')
#boolfuck('>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]>>>>>>>>>>>>>>>>>>>;>;>;>;>;>;>;>;<<<<<<<<>>>>>>>>>>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<>>>>>>>>>>>>>>>>>>>;>;>;>;>;>;>;>;<<<<<<<<<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<>>>>>>>>>>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<>>>>>>>>>>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<>;>;>;>;>;>;>;>;<<<<<<<<')
#boolfuck(';;;+;+;;+;+;+;+;+;+;;+;;+;;;+;;+;+;;+;;;+;;+;+;;+;+;;;;+;+;;+;;;+;;+;+;+;;;;;;;+;+;;+;;;+;+;;;+;+;;;;+;+;;+;;+;+;;+;;;+;;;+;;+;+;;+;;;+;+;;+;;+;+;+;;;;+;+;;;+;+;+;', "")

a = boolfuck(">,>,>,>,>,>,>,>,>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]>;>;>;>;>;>;>;>;>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]>,>,>,>,>,>,>,>,>+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]","Codewars")
print(a)


