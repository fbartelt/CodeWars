import itertools as it
def firstn(generator, n):
    g = generator()
    for _ in range(n):
        yield next(g)
def erat2a( ):
    D = {  }
    yield 2
    for q in it.islice(it.count(3), 0, None, 2):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = q + 2*p
            while x in D:
                x += 2*p
            D[x] = p
def solve(a, b):
    return ''.join(str(q) for q in firstn(erat2a, a+b))[a:a+b]
print(solve(10000,5))