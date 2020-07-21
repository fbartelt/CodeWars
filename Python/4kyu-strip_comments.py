
import re
def solution(string,markers):
    if not markers:
        return string
    else:
        print(string)
        pattern = '([^\n\S]?[\\' + '\\'.join(markers) + '][^\\\n]*)'
        t = re.subn(pattern, "", string)
        print("t",t[0])
        return t[0]
solution("apples, pears § and bananas\ngrapes\navocado *apples",['*', '§'])
