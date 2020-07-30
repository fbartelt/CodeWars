module Fib where

fib :: Int -> Int
fib = (map fibm [0..] !!)
    where fibm 1 = 0
          fibm 2 = 1
          fibm n = fib (n-1) + fib (n-2)