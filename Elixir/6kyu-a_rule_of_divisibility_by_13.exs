defmodule Divisible13 do

  def thirtx(n) do
    arr = [1,10,9,12,3,4]
    dig = Enum.reverse(Integer.digits(n))
    dig = Enum.sum(Enum.map(0..Enum.count(dig)-1,fn x ->
    Enum.at(dig, x) * Enum.at(arr,Integer.mod(x,6)) end))
  end

  def thirt(n) do
    dig = thirtx(n)
    cond do
      dig != thirtx(dig)->
        dig = thirtx(dig)
        thirt(dig)
      true -> dig
    end
  end

end
