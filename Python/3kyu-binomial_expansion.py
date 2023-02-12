# %%
import re
from math import comb
from functools import reduce


def expand(expr):
    s1, a, x, s2, b, n = re.findall(r'\((-*)(\d*)(\w)([+-])(\d+)\)\^(\d+)', expr)[0]
    a = (-1)**(s1 == '-') * int(a or 1)
    b = (-1)**(s2 == '-') * int(b)
    n = int(n)
    poly = [str(comb(n, k) * a**(k) * b**(n-k)) + f"{x if k > 0 else ''}{'^'+f'{k}' if k>1 else ''}" for k in range(n, -1, -1)]
    poly = [p for p in poly  if p[0]!='0']
    poly = re.sub(r'(^|\D)1([a-zA-Z])', r'\1\2', reduce(lambda i, j: i+j if j[0] == '-' else i+'+'+j, poly))

    return poly


# %%
"""TESTS"""
print(expand("(x+1)^2"))    # returns "x^2+2x+1"
print(expand("(p-1)^3"))    # returns "p^3-3p^2+3p-1"
print(expand("(2f+4)^6"))   # returns "64f^6+768f^5+3840f^4+10240f^3+15360f^2+12288f+4096"
print(expand("(-2a-4)^0"))   # returns "1"
print(expand("(-12t+43)^2")) # returns "144t^2-1032t+1849"
print(expand("(r+0)^203"))  # returns "r^203"
print(expand("(-x-1)^2"))    # returns "x^2+2x+1"

# %%
