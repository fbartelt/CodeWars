defmodule SongDecoder do
  def decode_song(song) do
    String.split(song,"WUB",trim: true) |> Enum.join(" ")
  end
end
