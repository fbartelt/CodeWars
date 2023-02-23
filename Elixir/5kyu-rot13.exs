defmodule Encryptor do
  def rot13(str) do
    Enum.map(String.to_charlist(str), fn x ->
      cond do
        Enum.any?(?a..?z, fn y -> y == x end) ->
          Integer.mod(Integer.mod(x + 13,97),26) + 97
        Enum.any?(?A..?Z, fn y -> y == x end) ->
          Integer.mod(Integer.mod(x + 13,65),26) + 65
        true ->
          x
      end
    end)
    |> to_string
  end
end
