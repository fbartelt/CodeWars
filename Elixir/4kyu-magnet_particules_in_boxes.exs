defmodule Magnet do
  def  pow(n, k), do: pow(n, k, 1)
  defp pow(_, 0, acc), do: acc
  defp pow(n, k, acc), do: pow(n, k - 1, n * acc)

  def doubles(maxk, maxn) do
    vec_list = (Enum.map(1..maxk, fn x -> [0] ++ (for y <- 1..maxn, do: 1/(x*pow(y+1,2*x)) )end))
    vec = Enum.sum(for x <- vec_list, do: Enum.sum(x))
  end

end
