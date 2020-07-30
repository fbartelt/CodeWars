def interpreter(code, iterations, width, height):
    pos, matrix = [0,0], {row:[0]*width for row in range(height) }
    i = loop = iter_ = 0
    while i < len(code) and iter_ < iterations:
        command = code[i]
        if loop:
            if command == '[':
                loop += 1
            elif command == ']':
                loop -= 1
        elif command in ['e','w']:
            pos[1] = (pos[1] + (-1)**(command=='w')) % width
        elif command in ['n','s']:
            pos[0] = (pos[0] + (-1)**(command=='n')) % height
        elif command == '*':
            matrix[pos[0]][pos[1]] ^= 1
        elif command == '[' and matrix[pos[0]][pos[1]] == 0:
            loop += 1
        elif command == ']' and matrix[pos[0]][pos[1]] == 1:
            loop -= 1
        elif command not in ['n','s','e','w','[',']','*']:
            iter_-=1
        i += 1 if not loop else loop // abs(loop)
        if not loop: iter_ +=1 
    string = '\r\n'.join(''.join(str(row) for row in matrix[rows]) for rows in matrix.keys())
    print(string)
    return string
interpreter('   *   [[s*en]   sw[w]enn   [[e]w*ssss*nnnnw[w]ess[e]*[w]enn]   ssss[*nnnn*essss]   nnnnw[w]e   ss]', 3000, 30, 30)