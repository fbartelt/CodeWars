import re
operators = {
    '+' : lambda x,y : x+y,
    '-' : lambda x,y : x-y,
    '*' : lambda x,y : x*y,
    '/' : lambda x,y : x/y,
}
op_high = re.compile(r'(-{0,1}\d+\.*\d*)*\s*([\/\*])\s*(-{0,1}\d+\.*\d*)')
op_low = re.compile(r'(-{0,1}\d+\.*\d*)*\s*([\+\-])\s*(-{0,1}\d+\.*\d*)')
parenthesis = re.compile(r'\(([^\(]+?)\)')
class Calculator(object):
  def evaluate(self, string):
    par = re.search(parenthesis,string)
    while par:
        result = evaluate(par[1])
        string = re.sub(parenthesis, result, string,1)
        print(string)
        par = re.search(parenthesis,string)
    residue = re.search(r'[\+\-\/\*]',string)
    while residue:
        string = evaluate(string)
        residue = re.search(r'([\+\-\/\*])(?:\D)',string)
    print("FINAL", float(string))
    return float(string)
def evaluate(expression):
    calculations = True
    while calculations:
        print("EXP",expression)
        high = re.search(op_high, expression)
        low = re.search(op_low, expression)
        if high: 
            print(high[1],high[2],high[3])
            result = operators[high[2]](float(high[1]),float(high[3]))
            print(result)
            print(re.escape(high[0]))
            expression = re.sub(re.escape(high[0]), str(result), expression)
        elif low:
            result = operators[low[2]](float(low[1] or 0),float(low[3]))
            print(result)
            expression = re.sub(re.escape(low[0]), str(result), expression)
        else:
            result = expression
        calculations = re.search(r'([\+\-\/\*])(?:\D)',expression)
    return str(result)