module MultiplesOf3And5 where

solution :: Integer -> Integer
solution number = sum[x |x<-[1..number-1] , x `mod`3==0 || x`mod`5==0]