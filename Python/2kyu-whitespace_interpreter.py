# to help with debugging
import re
def unbleach(n):
    return n.replace(' ', 's').replace('\t', 't').replace('\n', 'n')

# solution
def whitespace(code, inp = ''):
    output = ''
    stack, subroutines = [], []
    heap, label_dict = {}, {}
    imp_dict = {' ': 1, '\t ' : 2, '\t\t': 3 , '\t\n': 4, '\n': 5 }
    #       stack  arithmetic    heap    input/output  flow control
    imps = []
    inp = list(inp)
    code = ''.join([char for char in code if char in [' ', '\n', '\t']])
    print(list(code))
    control = 0
    if not code: raise SyntaxError('non command')
    while control < len(code):
        print('stack', stack, 'heap', heap)
        cmd = code[control]
        if cmd == ' ': ##IMP STACK
            print('STACK')
            print('haro', control)
            imps.append(1)
            control += stack_manipulation(code[control+1 :], stack)
            print('Ó O BICHO',stack)
            print(control)
            print(list(code))
            #break
        elif cmd == '\t':
            if code[control+1] == ' ':
                print('ARITH')
                arithmetic(code[control+2: control+4], stack)
                control += 4
            elif code[control+1] == '\t':
                print('HEAP')
                print('HERRE')
                print(list(code[control:]))
                print(list(code[control+2:control+4]))
                print('HHHH')
                heap_access(code[control+2: control+3], stack, heap)
                control += 3
            elif code[control+1] == '\n':
                print('INPUT')
                inp, output = input_output(code[control+2: control+4], stack, heap, inp, output)
                print('DUNN',list(code[control:control+4]), code[control+3])
                print('heap==',heap, 'stack==',stack)
                control += 4
        elif cmd == '\n':
            print('FLOW')
            print(list(code[control:]))
            #break
            print('CONTROL 111', control)
            control = flow_control(code, control+1, stack, label_dict, subroutines)
            print('dict',label_dict)
            print('CONTROL 222', control)
            if control == -1:
                print('brekou')
                print('stack == ', stack, 'heap == ', heap, 'dict == ', label_dict)
                break
        else: 
            raise SyntaxError('non command')
    print(output)
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
    print('code == ', list(code))
    i = 0
    command = code[i]
    print(list(code[:2]))
    if command == ' ':
        _i, number = parse_number(code[1:])
        print(number,'kk')
        stack.append(number)
        print(i, _i)
        i+= 1+_i
    elif command == '\t':
        command = code[i+1]
        _i, number = parse_number(code[2:])
        print('number == ', number, -number-2)
        if command == ' ':
            if number<0: raise ValueError('orno')
            number = -number-1
            print(number)
            if number not in range(-len(stack), len(stack)):
                raise ValueError("Stack index doesn't exist")
            else:
                stack.append(stack[number])
        elif command == '\n':
            print('slide', number)
            if number < 0 or number >= len(stack):
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
        if command == ' ':
            stack.append(stack[-1])
        elif command == '\t':
            stack.extend([stack.pop(), stack.pop()])
        elif command == '\n':
            stack.pop()
        i += 2
    return i+1  ## TALVEZ RETORNAR I+1 SEJA MAIS PRATICO

def arithmetic(command, stack):
    #command = code[0:2]
    if len(stack) < 2: raise ValueError('Attempting arithmetic with stack with less than 2 numbers')
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
    print(stack)
    
def heap_access(command, stack, heap): ## command = code[i:i+2]
    if len(stack) == 0 : raise ValueError('Empty stack')
    a = stack.pop()
    if command == ' ':
        if len(stack) == 0 : raise ValueError('Stack too short to pop twice')
        heap.update({stack.pop() : a})
    elif command == '\t':
        if a in heap.keys():
            stack.append(heap[a])
        else: 
            raise ValueError('Heap address not found')

def input_output(command, stack, heap, inp, output):
    print('cehogu oq', stack, list(command))
    print('in',inp)
    if command == '  ':
        output += chr(stack.pop())
    elif command == ' \t':
        output += str(stack.pop())
    elif command == '\t ':
        heap.update({stack.pop() : ord(inp.pop(0))})
    elif command == '\t\t':
        number , num_s = inp.pop(0), ''
        print('ff', list(number),list(num_s))
        while number != '\n':
            num_s += number
            number = inp.pop(0) 
        heap.update({stack.pop() : int(num_s)})
    return inp, output

def flow_control(code, idx, stack, label_dict, subroutines):
    command = code[idx:idx+2]
    if command[0] == ' ':
        print('deu espaço')
        i, label = parse_label(code[idx+2:])
        print(list(code[i:]))
        if command[1] == ' ':
            print('esp esp')
            label_dict.update({label : idx+2+i})
            i += idx+2
        elif command[1] in ['\t', '\n']:
            if label in label_dict.keys():
                print('wut')
                print(list(label), label_dict)
                if command[1] == '\t' : subroutines.append(idx+2+i)
                i = label_dict[label]
            else:
                m = re.search(r'(\n  ' + label + '\n)', code[i:])
                print(m)
                return -1
                if m:
                    if command[1] == '\t' : subroutines.append(idx+2+i)
                    i += m.start()
                else:
                    raise ValueError('Label undefined')
    elif command[0] == '\t':
        i, label = parse_label(code[idx+2:])
        value = stack.pop()
        if (not value and command[1] == ' ') or (value < 0 and command[1] == '\t'):
            print(stack, value)
            if label in label_dict.keys():
                print('something wrong')
                return -1
                i = label_dict[label]
            else:
                print('searching for label', list(label))
                m = re.search(r'(\n  ' + label + '\n)', code[i:])
                print(m, )
                #return -1
                if m:
                    i += m.start()+idx+2
                else:
                    raise ValueError('Label undefined')
        else:
            i += idx+2
    elif command == '\t\n':
        i = subroutines.pop()
    elif command == '\n\n':
        i = -1
    return i 




#print(arithmetic('\t\t',[1,2,3,4]))
#print(stack_manipulation(' 				 	 	 \n',[1,2,3]))
#whitespace('   \t  as//  / \t\n\t\n bbb \n\n\n')
unb = 'ssstntnstntssnssstnnsssnnnn'
code = unb.replace('s', ' ').replace('t', '\t').replace('n', '\n')
whitespace(code, '')
#import re
# mm = re.search(r'(\n  ([^\S\t\n]*?)\n)', code)
# print(list(mm[0]),list(mm[2]))
#print(parse_number(' 				 	 	 \n'))


