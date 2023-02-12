#%%
import re
import numpy as np
from functools import reduce

def map_poly(poly):
    coefs = [0]*(int(poly[-1][-1] or (poly[-1][-2] != '')) + 1)
    for p in poly:
        s1, a, x, n = p
        a = (-1)**(s1 == '-') * int(a or 1)
        n = n or (x != '')
        coefs[int(n) or 0] = a
    
    return coefs, x

def polynomial_product(polynomial_1: str, polynomial_2: str) -> str:
    split = re.compile(r'([-+]*)(\d*)([A-Za-z]*)\^*(\d*)')
    p1 = sorted(split.findall(polynomial_1.replace(' ', '')), key=lambda x : (int(x[3] or 0), x[2]), reverse=True)
    p2 = sorted(split.findall(polynomial_2.replace(' ', '')), key=lambda x : (int(x[3] or 0), x[2]), reverse=True)
    p1, x = map_poly(p1[-2::-1])
    p2, y = map_poly(p2[-2::-1])
    x = x or y
    result = np.convolve(p1[::-1], p2[::-1])
    result = [f"{r }"+f"{x if i>0 else ''}"+f"{'^'+str(i) if i>1 else ''}" for i, r in enumerate(result[::-1])]
    result = [p for p in result[::-1]  if p[0]!='0']
    if len(result) > 0:
        result = re.sub(r'(^|\D)1([a-zA-Z])', r'\1\2', reduce(lambda i, j: i+j if j[0] == '-' else i+'+'+j, result))
    else:
        result = '0'
    return result

#%%
print(polynomial_product("u^2 + 2u+1", "u + 1"))
print(polynomial_product("x^2", "3x - 1"))
print(polynomial_product("-4r^2 + 1", "-1"))
print(polynomial_product("1", "p^3"))
print(polynomial_product("1", "-1") )
print(polynomial_product("0", "2 - x") )
print(polynomial_product("-1", "0"))
print(polynomial_product("v^2 - 1+3v^3", "1+v^2"))
print(polynomial_product("-10i^13 - i + 152i^101", "-3 -98i^34 + 7i^2 - 4i"))

# %%
