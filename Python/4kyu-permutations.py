import itertools
def permutations(string):
    return list(set(''.join(p) for p in itertools.permutations(string)))
