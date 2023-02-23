defmodule GuessIt do
  def guess(n, m) do
    # r = 5n - m -2b // g= m -4n +b
    sol_vec = Enum.map(Enum.filter(((4*n) - m)..div(((5*n) - m),2), fn x -> x>= 0 end), fn b -> {m - (4*n) + b, (5*n) - m - (2*b), b} end )
  end
end
