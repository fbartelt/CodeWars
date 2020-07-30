module Century where

century::Int -> Int
century years = (years`div`100)+x
  where x | years `mod`100 == 0 = 0 
          | otherwise = 1