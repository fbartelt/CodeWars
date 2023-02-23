defmodule ParenthesesValidator do
  def valid_parentheses(string) do
    subb = Regex.replace(~r/[^\(\)]+/, string,"")
    sub = Regex.replace(~r/\(\)/,subb,"")
    cond do
      Regex.match?(~r/\(\)/, sub) -> valid_parentheses(sub)
      sub == "" -> true
      true -> false
    end
  end
end
