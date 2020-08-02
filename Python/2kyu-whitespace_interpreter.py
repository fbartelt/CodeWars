# to help with debugging
def unbleach(n):
    return n.replace(' ', 's').replace('\t', 't').replace('\n', 'n')

# solution
def whitespace(code, inp = ''):
    output = ''
    stack = []
    heap = {}
    imps = {' ': 1, '\t ' : 2, '\t\t': 3 , '\t\n': 4, '\n': 5 }
    #       stack  arithmetic    heap    input/output  flow control
    for cmd in code:
        print(cmd, ascii(cmd), cmd=='\t')
    #...
    return output

whitespace('   \t   \n            ')