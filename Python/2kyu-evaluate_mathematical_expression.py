import re
operators = {
    '+' : lambda x,y : x+y,
    '-' : lambda x,y : x-y,
    '*' : lambda x,y : x*y,
    '/' : lambda x,y : x/y,
    '@' : lambda x : -x,
}
priorities = {
    '@' : 4,
    '/' : 3,
    '*' : 3,
    '+' : 2,
    '-' : 2,
    '(' : 1,
}

def changes(expression):
    exp = re.sub(r'^\-([0-9]+\.{0,1}[0-9]*)|([\-\+\/\*\(])\s*\-([0-9]+\.{0,1}[0-9]*)', r'\g<1>\g<2>@\g<3>',expression)
    exp = re.sub(r'\-(\()', r'@\g<1>', exp)
    return exp

def split(string):
    cc = re.split(r'\s*([0-9]+\.{0,1}[0-9]*)\s*|\s*([\(\+\-\*\/@\)])\s*',string)
    cc = [l for l in cc if (l!='' and l!= None)]
    return cc

def reverse_polish(expression):
    expression = changes(expression)
    operations = [] 
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
    return rpn

def calc(expression):
    rpn = reverse_polish(expression)
    numbers = []
    for token in rpn:
        if token not in ['*','/','-','+','@']:
            numbers.append(float(token))
        else:
            if(token == '@'):
                numbers.append(operators[token](numbers.pop()))
            elif(token == '-' and len(numbers) < 2):
                numbers.append(operators['@'](numbers.pop()))
            else:
                second = numbers.pop()
                first = numbers.pop()
                numbers.append(operators[token](first,second))
    return numbers[0]
a = calc('(63) * (58 / 13 * -(10)) + (-62 * -(((-(2 - 82)))) / 35)')
print(a)
