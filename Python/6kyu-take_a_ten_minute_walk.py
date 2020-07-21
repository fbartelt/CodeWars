import numpy as np
def is_valid_walk(walk):
    if not(np.size(walk) == 10):
        return False
    else:
        h = walk.count('e')-walk.count('w')
        v = walk.count('n')-walk.count('s')
        return True if h==0 and v==0 else False
    #determine if walk is valid
    pass