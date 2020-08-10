import re

def whitespace(code, inp = ''):
    output = ''
    stack, subroutines = [], []
    heap, label_dict = {}, {}
    inp = list(inp)
    code = ''.join([char for char in code if char in [' ', '\n', '\t']])
    control = 0
    if not code: raise SyntaxError('non command')
    while control < len(code):
        cmd = code[control]
        if cmd == ' ': 
            control += stack_manipulation(code[control+1 :], stack)
        elif cmd == '\t':
            if code[control+1] == ' ':
                arithmetic(code[control+2: control+4], stack)
                control += 4
            elif code[control+1] == '\t':
                heap_access(code[control+2: control+3], stack, heap)
                control += 3
            elif code[control+1] == '\n':
                inp, output = input_output(code[control+2: control+4], stack, heap, inp, output)
                control += 4
        elif cmd == '\n':
            control = flow_control(code, control+1, stack, label_dict, subroutines)
            if control == -1:
                break
        else: 
            raise SyntaxError('non command')
    if control != -1:
        err = 'Subroutine does not exit or return' if subroutines else 'Unclean termination'
        raise SyntaxError(err)
    return output

def parse_number(code):
    i, bit_list, number = 0, [], 0
    if code[i] == '\n':
        raise ValueError('Number should have at least a [sign] symbol') 
    while code[i] != '\n':
        bit_list.append(int(code[i] == '\t'))
        i += 1
    if len(bit_list) > 1:
        for bit in bit_list[1:]:
            number = number * 2 + bit
        number = (-1)**(bit_list[0] == 1)*number
    return i+1, number

def parse_label(code):
    label, i = '', 0
    while code[i]!= '\n':
        label += code[i]
        i += 1
    return i+1, label

def stack_manipulation(code, stack):
    i = 0
    command = code[i]
    if command == ' ':
        _i, number = parse_number(code[1:])
        stack.append(number)
        i+= 1+_i
    elif command == '\t':
        command = code[i+1]
        _i, number = parse_number(code[2:])
        if command == ' ':
            if number<0: 
                raise IndexError('Invalid Stack Index')
            number = -number-1
            if number not in range(-len(stack), len(stack)):
                raise IndexError("Stack index doesn't exist")
            else:
                stack.append(stack[number])
        elif command == '\n':
            if not stack:
                raise IndexError('Empty Stack')
            elif number < 0 or number >= len(stack):
                top = stack.pop()
                stack.clear()
                stack.append(top)
            else:
                top = stack.pop()
                for _ in range(number):
                    stack.pop()
                stack.append(top)
        i += 2 + _i
    elif command == '\n':
        command = code[i+1]
        if not stack:
                raise IndexError('Empty Stack')
        elif command == ' ':
            stack.append(stack[-1])
        elif command == '\t':
            stack.extend([stack.pop(), stack.pop()])
        elif command == '\n':
            stack.pop()
        i += 2
    else:
        raise NameError('Invalid command for Stack')
    return i+1

def arithmetic(command, stack):
    if command not in ['  ', ' \t', ' \n', '\t\t', '\t ']:
        raise NameError('Invalid command for Arithmetic')
    if len(stack) < 2: 
        raise ValueError('Attempting arithmetic with stack with less than 2 numbers')
    if command == '  ':
        stack.append(stack.pop() + stack.pop())
    elif command == ' \t':
        stack.append(-(stack.pop()-stack.pop()))
    elif command == ' \n':
        stack.append(stack.pop() * stack.pop())
    elif command[0] == '\t':
        div_mod = {' ': lambda x,y : x//y , '\t': lambda x,y : x%y}
        a = stack.pop()
        if a == 0: raise ValueError('Division by 0')
        stack.append(div_mod[command[1]](stack.pop(), a))
    
def heap_access(command, stack, heap):
    if command not in [' ','\t']: 
        raise NameError('Invalid command for Heap Access')
    if len(stack) == 0 : 
        raise ValueError('Empty stack')
    a = stack.pop()
    if command == ' ':
        if len(stack) == 0 : raise ValueError('Stack too short to pop twice')
        heap.update({stack.pop() : a})
    elif command == '\t':
        if a in heap.keys():
            stack.append(heap[a])
        else: 
            raise IndexError('Heap address not found')

def input_output(command, stack, heap, inp, output):
    if not stack:
        raise IndexError('Not enough elements in stack')
    elif command == '  ':
        output += chr(stack.pop())
    elif command == ' \t':
        output += str(stack.pop())
    elif command == '\t ':
        heap.update({stack.pop() : ord(inp.pop(0))})
    elif command == '\t\t':
        number , num_s = inp.pop(0), ''
        while number != '\n':
            num_s += number
            number = inp.pop(0) 
        heap.update({stack.pop() : int(num_s)})
    else:
        raise NameError('Invalid command for Input/Output')
    return inp, output

def flow_control(code, idx, stack, label_dict, subroutines):
    command = code[idx:idx+2]
    if command[0] == ' ':
        i, label = parse_label(code[idx+2:])
        if command[1] == ' ':
            if label in label_dict.keys():
                raise ValueError('Label already defined')
            else:
                label_dict.update({label : idx+2+i})
            i += idx+2
        elif command[1] in ['\t', '\n']:
            if label in label_dict.keys():
                if command[1] == '\t' : subroutines.append(idx+2+i)
                i = label_dict[label]
            else:
                m = re.search(r'(\n  ' + label + '\n)', code[i:])
                if m:
                    if command[1] == '\t' : subroutines.append(idx+2+i)
                    i += m.start()
                else:
                    raise ValueError('Label undefined')
    elif command in ['\t ','\t\t']:
        i, label = parse_label(code[idx+2:])
        if stack: 
            value = stack.pop()
        else:
            raise IndexError('Trying to pop from empty Stack')
        if (not value and command[1] == ' ') or (value < 0 and command[1] == '\t'):
            if label in label_dict.keys():
                i = label_dict[label]
            else:
                m = re.search(r'(\n  ' + label + '\n)', code[idx+2+i:])
                if m:
                    i += m.start()+idx+2
                else:
                    raise ValueError('Label undefined')
        else:
            i += idx+2
    elif command == '\t\n':
        if subroutines:
            i = subroutines.pop()
        else:
            raise SyntaxError('Return outside subroutine')
    elif command == '\n\n':
        i = -1
    else:
        raise NameError('Invalid command for Flow Control')
    return i 

### TO HELP WITH RANDOM WHITESPACE CODE (CHANGES ALL WHITESPACES TO READABLE CHARACTERS)
def unbleach(n):
    return n.replace(' ', 's').replace('\t', 't').replace('\n', 'n')



#print(arithmetic('\t\t',[1,2,3,4]))
#print(stack_manipulation(' 				 	 	 \n',[1,2,3]))
#whitespace('   \t  as//  / \t\n\t\n bbb \n\n\n')
unb = 'nstnnnnnssntntn'
code = unb.replace('s', ' ').replace('t', '\t').replace('n', '\n')
whitespace(code, '')


