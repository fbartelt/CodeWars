from gmpy2 import next_prime
   
P, n = '', 2
while len(P) < 21000:
    P += str(n)
    n = next_prime(n)
        
def solve(a, b):
    return P[a:a+b]