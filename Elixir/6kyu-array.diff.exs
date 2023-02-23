# NOT COMPLETED
defmodule ArrayDiff do
  def array_diff(a, b) do
    Enum.reject(a, fn _x -> Enum.find_value(b, fn y -> y==b end) end)
  end
end
