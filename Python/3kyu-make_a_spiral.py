# %%
import numpy as np

def spiralize(size):
    spiral = np.array([[0]*size]*size)
    for i in range(size):
        match i % 4:
            case 0:
                spiral[int(i/2), (int(i/2) - 1)*(i != 0) : size-int(i/2)] = 1
            case 1:
                spiral[int((i + 1)/2) : size-int((i-1)/2), size-int((i + 1)/2)] = 1
            case 2:
                spiral[size-int(i/2), int((i - 2)/2) : size-int(i/2)] = 1
            case 3:
                spiral[int((i + 1)/2) : size-int((i - 1)/2), int((i - 3)/2)] = 1
 
    return spiral.tolist()


# %%
s = spiralize(14)
print(np.array(s))
# %%
