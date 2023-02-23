defmodule Kata do
  def permutation_by_number(word,n) do
    word
    |> Frequency.map_frequency
    |> (&(cond do
      Factorial.valid_perm(&1)>= (n+1) -> aux(&1,n+1)
      true -> [""] end)).()
    |> List.to_string
  end

  def aux(map, m, c \\ [], t \\ 0) do
    cond do
      Enum.empty?(map) -> c
      true ->
        char = Enum.at(Map.keys(map),t)
        map = Map.update!(map,char, &(&1-1))
        tot = Factorial.valid_perm(map)
        cond do
          tot >= m ->
            cond do
              map[char]==0 -> aux(Map.delete(map,char), m, List.flatten([c|[char]]))
              true -> aux(map, m, List.flatten([c|[char]]))
            end
          true ->  aux(Map.update!(map,Enum.at(Map.keys(map),t), &(&1+1)), m-tot,c,t+1)
        end
    end
  end
end

defmodule Frequency do
def map_frequency(word) do
  a = word
  |> String.graphemes
  |> Enum.sort
  |> Enum.group_by(&(&1))
  for {key, val} <- a, into: %{}, do: {key, Enum.count(val)}
end
end

defmodule Factorial do
def fact(0), do: 1
def fact(n) when n > 0 do
  Enum.reduce(1..n, &*/2)
end

def valid_perm(map) do
  fact(Enum.sum(Map.values(map)))/Enum.reduce(Map.keys(map),1, fn x,acc -> fact(map[x])*acc end)
end
end
