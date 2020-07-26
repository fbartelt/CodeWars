def interpreter(code, tape):
    dic = {'<':-1, '>':1}
    tape = [int(ch) for ch in list(tape)]
    pos = 0
    i = 0 
    stack = []
    while i < len(code):
        command = code[i]
        if pos < 0 or pos >= len(tape):
            break 
        elif command in ['<','>']:
            pos+= dic[command]
        elif command == '*':
            tape[pos]=int(not tape[pos])
        elif command == '[' and tape[pos] == 0:
            stack.append(i)
            while stack:
                i+=1
                if code[i] == '[':
                    stack.append(i)
                elif code[i] == ']':
                    stack.pop()
        elif command == ']' and tape[pos] == 1:
            stack.append(i)
            while stack:
                i-=1
                if code[i] == ']':
                    stack.append(i)
                elif code[i] == '[':
                    stack.pop()
        i+=1
    return ''.join([str(num) for num in tape])
res = interpreter('*[>*]', "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
print(res)
