import re

operators = {
    '+' : lambda x,y : x+y,
    '-' : lambda x,y : x-y,
    '*' : lambda x,y : x*y,
    '/' : lambda x,y : x/y,
    '%' : lambda x,y : x%y,
    '@' : lambda x : -x,
}

priorities = {
    '@' : 10,
    '/' : 9,
    '*' : 9,
    '%' : 9,
    '+' : 8,
    '-' : 8,
    '=' : 7,
    '(' : 6,
    '=>' : 5,
    'fn' : 4,
}

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

def reverse_polish(tokens):
    operations = [] 
    rpn = []
    for token in tokens:
        is_operand = (re.match(r'[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+', token)) and (token != 'fn')
        if is_operand:
            rpn.append(token)
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

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        rpn = reverse_polish(tokens)
        print(rpn)
        try:
            return self.eval(reverse_polish(tokens))
        except Exception:
            print('err')
        
        
#         if tokens[0] == 'fn':
#             pass
#         elif '=' in tokens:
#             pass
#         else:
#             print(reverse_polish(tokens))
#             var_list = []
#             last = tokens[0]
#             for token in tokens[1::]:
#                 if token == '=':
#                     var_list.append(last)
#             return self.eval(reverse_polish(tokens))
    def remove_cycles(self):
        cycles = [x for x, y in enumerate(self.vars.values()) if y in self.vars.keys()]
        while cycles:
            self.vars[list(self.vars.keys())[cycles[0]]] = self.vars[self.vars[list(self.vars.keys())[cycles[0]]]]
            cycles = [x for x, y in enumerate(self.vars.values()) if y in self.vars.keys()]
    
    def create_function(self):
        pass
    
    def eval(self, rpn):
        numbers = []
        for token in rpn:
            if (token not in operators.keys()) and (token != '='):
                if re.match(r'[a-zA-Z_]', token):
                    numbers.append(self.vars.get(token, token))
                else:
                    numbers.append(float(token))
            else:
                if(token == '@'):
                    numbers.append(operators[token](numbers.pop()))
                elif(token == '='):
                    last = numbers.pop()
                    self.vars[numbers.pop()] = last
                    numbers.append(last)
                elif(token == '-' and len(numbers) < 2):
                    numbers.append(operators['@'](numbers.pop()))
                else:
                    second = numbers.pop()
                    first = numbers.pop()
                    numbers.append(operators[token](first,second))
            self.remove_cycles()
        result = numbers[0]
        if isinstance(result, str):
            result = self.vars.get(result, None)
        return result

intt = Interpreter()
print(intt.input('fn avg x y => (x + y)/2'))
print(intt.input('x = 29 + (y = 11)'))
print(intt.vars)
print(intt.input('x'))