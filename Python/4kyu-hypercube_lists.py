import numpy as np
a = [[2, 3], 4, 5, 6, [2, [2, 3, 4, 5], 2, 1, 2], [[[[1]]]], [],3]
for i in a:
    print(isinstance(i, list))
d=[]
l=[]
def dive(lista, last=0):
    for idx, item in enumerate(lista):
        if isinstance(item, list):
            d.append(last+1)
            l[idx]+=len
