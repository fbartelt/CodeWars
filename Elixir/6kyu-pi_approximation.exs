defmodule Piapprox do
  def trunca(num), do: (trunc num * :math.pow(10,10)) / :math.pow(10, 10)
  def loop(value,n,epsilon) do
    series = fn x -> :math.pow(-1, x)/(2*x + 1) end
    s = Enum.sum([value|[series.(n)]])
    if abs((4*value) - :math.pi) > epsilon, do: loop(s, n+1, epsilon), else: [n,trunca(4*value)]
  end
  def iter_pi(epsilon) do
    value = 0
    loop(value,0,epsilon)
  end
end
