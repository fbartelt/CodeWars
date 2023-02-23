defmodule PokerHand do
  @result %{win: 1, loss: 2, tie: 3}
  @cards %{"T" => 10, "J" => 11, "Q" => 12, "K" => 13, "A" => 14}
  def rank(hand) do
    #0-> high card, 1->pair, 2-> 2 pairs, 3-> three of a kind, 4-> straight, 5-> flush, 6-> full house
    #7->four of a kind, 8-> straight flush (also royal)
    hc = Enum.map(hand, fn x->Enum.at(x,0) end)
    group = Enum.map((Enum.group_by(hc, &(&1)) |> Map.values), fn x -> [length(x), Enum.at(x,0)] end)
            |> Enum.sort(&(&1 >= &2 )) |> List.zip
    cond do
      Enum.count(hand, fn x -> Enum.at(Enum.at(hand,0),1) == Enum.at(x,1) end) == 5 ->
        cond do
          Enum.to_list(Enum.at(hc,0)..Enum.at(hc,4)) == hc ->
            [8|[hc]]
          true ->
            [5|[hc]]
        end
      Enum.to_list(Enum.at(hc,0)..Enum.at(hc,4)) == hc ->
        [4|[hc]]

      true ->
        case Enum.at(group, 0) do
          {1,1,1,1,1} -> [0|[Tuple.to_list(Enum.at(group,1))]]
          {2,1,1,1} -> [1|[Tuple.to_list(Enum.at(group,1))]]
          {2,2,1} -> [2|[Tuple.to_list(Enum.at(group,1))]]
          {3,1,1} -> [3|[Tuple.to_list(Enum.at(group,1))]]
          {3,2} -> [6|[Tuple.to_list(Enum.at(group,1))]]
          {4,1} -> [7|[Tuple.to_list(Enum.at(group,1))]]

        end

    end
  end
  def mk_hand(player) do
    Enum.map(String.split(player), fn x -> String.codepoints(x) end)
    |> Enum.map(fn x ->
         cond do
           Map.has_key?(@cards, Enum.at(x,0)) == false -> [String.to_integer(Enum.at(x,0)), Enum.at(x,1)]
           true -> [Map.get(@cards,Enum.at(x,0)), Enum.at(x, 1)]
         end
       end)
    |> Enum.sort(&(&1 >= &2))
    |> rank
  end

  def compare(player, opponent) do
    p1 = mk_hand(player)
    p2 = mk_hand(opponent)
    cond do
      Enum.at(p1, 0) > Enum.at(p2, 0) -> @result.win
      Enum.at(p1, 0) < Enum.at(p2, 0) -> @result.loss
      true ->
        cond do
          Enum.at(p1, 1) > Enum.at(p2, 1) -> @result.win
          Enum.at(p1, 1) < Enum.at(p2, 1) -> @result.loss
          true -> @result.tie
        end
    end
  end

end
