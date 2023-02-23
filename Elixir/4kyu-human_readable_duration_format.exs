defmodule DurationFormatter do
  @names %{ 0 => "year", 1 => "day", 2 => "hour", 3 => "minute", 4 => "second"}
  def format_duration(seconds) do
    cond do
      seconds == 0 ->
        vec = "now"
      true ->
        years = div(seconds,31536000)
        sec_rem = rem(seconds,31536000)
        days = div(sec_rem,86400)
        sec_rem = rem(sec_rem,86400)
        hours = div(sec_rem, 3600)
        sec_rem = rem(sec_rem, 3600)
        minutes = div(sec_rem, 60)
        sec = rem(sec_rem,60)
        vec = [years, days, hours, minutes, sec]
        |> Enum.map_reduce(0, fn x, acc -> { [to_string(x),
                                                    cond do
                                                      x > 1 ->
                                                        Enum.join([Map.get(@names,acc)]++["s"])
                                                      true ->
                                                        Map.get(@names,acc)
                                                    end
                                                  ], 1 + acc}
                                end)
        |> Tuple.to_list
        |> Enum.take(1)
        |> Enum.at(0)
        |> Enum.map(fn x -> List.to_tuple(x) end)
        |> List.flatten
        |> Enum.filter(fn x -> elem(x,0) != "0" end)
        |> Enum.map(fn x -> Tuple.to_list(x) end)
        |> Enum.map(fn x -> Enum.join(x, " ") end)
        cond do
          length(vec) > 1 ->
            Enum.join(Enum.at(Tuple.to_list(Enum.split(vec, length(vec) - 1)), 0), ", ") <>
            " and " <> Enum.at(vec, length(vec) - 1)
          true ->
            Enum.at(vec, 0)
        end
    end
  end
end
