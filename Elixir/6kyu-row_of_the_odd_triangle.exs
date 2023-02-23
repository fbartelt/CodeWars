defmodule OddRow do
  def triang_num(n) do
    tri_number = n*(n+1)/2
  end
  def odd_row(n) do
    row = :lists.seq(trunc(2*triang_num(n-1)+1),trunc((2*triang_num(n))-1), 2)
  end
end
