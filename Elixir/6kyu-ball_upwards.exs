defmodule Maxball do

  def max_ball(v0) do
    # your code
    v = v0/3.6
    g = 9.81
    _t_optimal = 10*(Kernel.round((v/g),1))
  end
end
