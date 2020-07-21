import re
priorities = {
    '^' : 4,
    '/' : 3,
    '*' : 3,
    '+' : 2,
    '-' : 2,
    '(' : 1,
}
def split(string):
    cc = re.split(r'\s*([\(\+\-\*\/\\^\)])\s*|\s*([0-9]+\.{0,1}[0-9]*)\s*',string)
    cc = [l for l in cc if (l!='' and l!= None)]
    return cc
def reverse_polish(expression):
    operations = [] # pilha de operações
    rpn = []
    token_list = split(expression)
    for token in token_list:
        is_operand = re.match(r'[0-9]+\.{0,1}[0-9]*', token)
        if is_operand:
            rpn.append(is_operand[0])
        elif token == '(':
            operations.append(token)
        elif token == ')':
            current = operations.pop()
            while current != '(':
                rpn.append(current)
                current = operations.pop()
        else:
            while operations and (priorities[operations[-1]] >= priorities[token]):
                rpn.append(operations.pop())
            operations.append(token)
    while operations:
        rpn.append(operations.pop())
    print(rpn)
    return ' '.join(rpn)

split('(2+2 - -2.0)*2.222 -7/ 8')
split('--1')
split('2- -1')
split('(((-3.0)))*7 + ((2-1)/7) -5')
split('2*8^7')
reverse_polish('2*8^7')