defmodule StringMix do

  def mix(s1, s2) do
    comparator = fn s, z -> cond do
                              String.length(s) == String.length(z) ->
                                s<=z
                              true -> String.length(s) >= String.length(z)
                            end
                  end

    comp = Enum.uniq(String.codepoints(s1<>s2))
    |> Enum.filter(fn x -> (x =~ ~r/^\p{Ll}$/u) end)
    map1 = Enum.map(comp, fn x -> [Enum.count(String.codepoints(s1), fn y ->
       String.contains?(x, y) end), x] end)
    map2 = Enum.map(comp, fn x -> [Enum.count(String.codepoints(s2), fn y ->
       String.contains?(x, y) end), x] end)
    cont = Enum.map((0..(length(comp)-1)), fn x ->
      cond do
        (Enum.at(map1,x) < Enum.at(map2,x)) and (Enum.at(Enum.at(map2,x),0)>1) ->
          [Enum.at(Enum.at(map2,x),0),Enum.at(comp,x),"2:"]
        (Enum.at(map1,x) > Enum.at(map2,x)) and (Enum.at(Enum.at(map1,x),0)>1) ->
          [Enum.at(Enum.at(map1,x),0),Enum.at(comp,x),"1:"]
        (Enum.at(map1,x) == Enum.at(map2,x)) and (Enum.at(Enum.at(map1,x),0)>1) ->
          [Enum.at(Enum.at(map1,x),0),Enum.at(comp,x),"=:"]
        true ->
          [-1,-1,-1]
      end
    end)
    |> Enum.map(fn x -> cond do
                          x == [-1,-1,-1] ->
                            ""
                          true ->
                            Enum.at(x,2)<> String.duplicate(Enum.at(x,1), Enum.at(x,0))
                        end
                end)
    |> Enum.sort(comparator)
    |> Enum.filter(fn x -> x != "" end)
    |> Enum.join("/")
  end
end
