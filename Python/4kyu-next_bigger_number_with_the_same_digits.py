def next_bigger(n):
    n = str(n)
    last = (n[-1],-1)
    for idx, current in enumerate(n[-2::-1]):
        if current < last[0]:
            possible = list(n[-idx-2:])
            bigger = [x for x in sorted(possible) if x > current][0]
            possible.remove(bigger)
            remnant = ''.join(sorted(possible))
            trial = n[:-idx-2]+bigger+remnant
            if trial > n:
                return int(trial)
        last = (n[-idx-2],-idx-2)
    return -1

print(next_bigger(6305064671193 ))

