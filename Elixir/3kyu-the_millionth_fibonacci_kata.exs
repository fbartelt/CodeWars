defmodule Fib do
  require Integer
  def fib(n) do
    cond do
      n<0 and Integer.is_even(n) -> -fib_iter(1, 0, 0, 1, -n)
      n<0 and Integer.is_odd(n) -> fib_iter(1, 0, 0, 1, -n)
      true -> fib_iter(1, 0, 0, 1, n)
    end
  end
  def fib_iter(a, b, p, q, count) do
    cond do
      count == 0 -> b
      Integer.is_even(count) -> fib_iter(a, b, (p*p)+(q*q), q*q+(2*p*q), div(count,2))
      true -> fib_iter((a*q+b*q+a*p), (b*p+a*q), p, q, count-1)
    end
  end
end
