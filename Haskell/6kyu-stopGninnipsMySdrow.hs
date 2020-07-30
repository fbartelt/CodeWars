spinWords :: String -> String
spinWords [] = []
spinWords a | xs /= [] =  b ++" " ++ spinWords(xs)
            | otherwise = b ++ spinWords(xs)
  where
    b | length(head(words a)) > 4 = reverse(head(words a))
      | otherwise = head(words a)
    xs = unwords(tail(words a))