def is_happy(n, vec=None):
    if vec is None:
        vec = [n]
    if n == 1:
        return True
    powd = sum([x**2 for x in [int(i) for i in str(n)]])
    if powd in vec:
        return False
    else:
        vec.append(powd)
        return is_happy(powd,vec)
