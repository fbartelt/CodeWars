defmodule Sumofdivided do
  def decomposition(n), do: decomposition(n, 2, [])
  defp decomposition(n, k, acc) when n < k*k, do: Enum.reverse(acc, [n])
  defp decomposition(n, k, acc) when rem(n, k) == 0, do: decomposition(div(n, k), k, [k | acc])
  defp decomposition(n, k, acc), do: decomposition(n, k+1, acc)

  def sum_of_divided(lst) do
    vec = Enum.map(lst, fn x -> {x,Enum.uniq(decomposition(abs(x)))} end)
    primes = Enum.map(vec, fn x -> elem(x, 1) end)
    |> List.flatten
    |> Enum.uniq
    |> Enum.map(fn x -> {x, Enum.sum(Enum.map(vec, fn y ->
                                            cond do
                                              Enum.any?(elem(y,1), fn z -> x==z end) == true ->
                                                elem(y,0)
                                              true ->
                                                0
                                            end
                                          end))}
                                        end)
    |> Enum.sort
  end

end
