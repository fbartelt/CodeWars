def bowling_score(frames):
    frames = [list(f) for f in frames.split(' ')]
    dicio = dict([(f, int(f) if f.isdigit() else 10) for g in frames for f in g ])
    for idx ,frame in enumerate(frames):
        if idx == 9:
            if '/' in frame:
                frames[9].pop(0)
            frames[idx] = sum(dicio[f] for f in frame)
        elif '/' in frame:
            next_score = sum(dicio[f] for f in frames[idx+1][0])
            frames[idx] = 10 + next_score
        elif 'X' in frame:
            frames[idx] = strike(frames[idx+1:],dicio)
        else:
            frames[idx] = sum(dicio[f] for f in frame)
    return sum(frames)
def strike(frames,dicio):
    if '/' in frames[0]:
        total = 20
    elif 'X' in frames[0]:
        if len(frames)>1:
            total = 20 + dicio[frames[1][0]]
        else:
            total = 20 + dicio[frames[0][1]]
    else:
        total = 10+sum(dicio[f] for f in frames[0])
    return total





game = 'X X 9/ 80 X X 90 8/ 7/ 44'
#game = '11 11 11 11 11 11 11 11 11 11'
#game = '00 00 00 00 00 00 00 00 X 0/X'
score = bowling_score(game)
print(score)