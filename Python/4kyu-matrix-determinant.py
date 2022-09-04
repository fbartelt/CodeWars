import numpy as np
def determinant(matrix):
    matrix = np.array(matrix)
    n, m = len(matrix), len(matrix[0])
    if n == 1:
        return matrix[0]
    else:
        signed_row = np.array(np.array([(-1)**(k%2) * e for k, e in enumerate(matrix[0, :])])).reshape(1, -1)
        subdets = [determinant([[matrix[x, y] for y in range(m) if y != j] for x in range(n) if x != 0]) for j, _ in enumerate(matrix[0])]
        det = (signed_row @ np.array(subdets)).flatten()[0]
        return det