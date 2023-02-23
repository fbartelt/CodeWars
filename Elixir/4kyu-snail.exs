defmodule Snail do

  def rotatem(matrix) do
    _rot = Enum.map(matrix, fn x -> Enum.reverse(x) end)
          |> List.zip
          |> Enum.map(&Tuple.to_list/1)
  end

  def snail( matrix ) do
    lines = length(matrix)
    columns = length(Enum.at(matrix,0))
    cond do
        (lines == 1) and (columns == 1) ->
          _path = matrix
        (lines == 1) and (columns == 0) ->
          _path = []
        true ->
          subm = List.delete(matrix, Enum.at(matrix,0))
          |> rotatem
          _path = [Enum.at(matrix,0)|snail(subm)]
          |> List.flatten
    end
  end

end
