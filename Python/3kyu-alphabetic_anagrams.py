import itertools
from math import factorial
from functools import reduce
def listPosition(word):
    sort = sorted(word)
    tot_rep =  dict((x,sort.count(x)) for x in set(sort))
    perms = 0
    for letter in word[:-1]:
        pos = sort.index(letter)
        sort.remove(letter)
        rep = reduce(lambda x,y: x*y, [factorial(tot_rep[let]) for let in set(sort)])
        perms += pos*factorial(len(sort))//rep
        tot_rep[letter]-=1
    return perms+1
print(listPosition('IMMUNOELECTROPHORETICALLY'))
#should equal 718393983731145698173