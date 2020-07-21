import numpy as np
board = [
            ['♟',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ','♟',' ',' ',' '],
            [' ',' ','♟','♟',' ',' ',' ',' '],
            [' ',' ','♔',' ',' ',' ','♜',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ']
        ]
arr = np.array(board)
i,j = np.where(arr == '♔')
king_pos = (int(i),int(j))
pieces = ['♛','♝','♞','♜','♟']
in_game = [x for x in pieces if x in arr ]
print(in_game)
a = np.where(arr=='♟')
a = [list(map(int,x)) for x in np.where(arr=='♟') ]
print(a)
if(king_pos[0]-1 in a[0] and (king_pos[1]-1 in a[1] or king_pos[1]+1 in a[1])): #pawn
    print("check")
b = list(map(lambda x: x in arr,pieces))
b

r = [list(map(int,x)) for x in np.where(arr=='♜') ]
if (king_pos[0] in r[0] or king_pos[1] in r[1]):
    print("check")


def king_is_in_check(chessboard):
    pieces = ['♛','♝','♞','♜','♟']
    arr = np.array(chessboard)
    i,j = np.where(arr == '♔')
    king_pos = (int(i),int(j))
    in_game = [x for x in pieces if x in arr ]
    pawn = [list(map(int,x)) for x in np.where(arr=='♟') ]
    if(king_pos[0]-1 in pawn[0] and (king_pos[1]-1 in pawn[1] or king_pos[1]+1 in pawn[1])):
        return True
