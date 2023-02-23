#NOT COMPLETED
defmodule Twice do
  def dbl_linear(n) do
    y = &(2*&1+1)
    z = &(3*&1+1)
    pos = %{y: 0, z: 0}
    Enum.reduce(0..n, [1], fn _x, acc -> cond do
      y.(Enum.at(acc,pos[:y])) < z.(Enum.at(acc,pos[:z])) ->
        pos = Map.update(pos, :y, 0, &(&1+1))
        IO.inspect(pos)
        IO.inspect(acc)
        List.flatten([acc|[y.(Enum.at(acc,pos[:y]-1))]])
      true ->
        Map.update(pos, :z, 0, &(&1+1))
        IO.inspect(pos)
        List.flatten([acc|[z.(Enum.at(acc,pos[:z]-1))]])
      end
     end)
  end
end

defmodule Test do
def test(n) do
Enum.reduce(1..n,%{y: 0, z: 0}, fn _x,acc -> cond do
  acc[:y]<acc[:z] ->
    Map.update(acc, :y, 0,&(&1+1))
  true -> Map.update(acc, :z,0, &(&1+1)) end
end)
end

def test2(n) do
  y = &(2*&1+1)
  z = &(3*&1+1)
  Enum.reduce(1..n,{%{y: 0, z: 0},[1]}, fn _x,acc -> cond do
    y.(elem(acc,0)[:y]) < z.(elem(acc,0)[:z]) ->
      Map.update(elem(acc,0), :y, 0,&(&1+1))
    true -> Map.update(acc, :z,0, &(&1+1)) end
    end)
end
end
