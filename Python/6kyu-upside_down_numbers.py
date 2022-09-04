mapper = {'0' : '0', '1' : '1', '6' : '9', '8' : '8', '9' : '6'}
def solve(a, b):
    count = 0
    for i in range(a, b):
        str_i = str(i)
        flipped = flipper(str_i, mapper)
        if flipped == str_i:
            mapper[str_i] = mapper.get(str_i, flipped)
            mapper[flipped] = mapper.get(flipped, str_i)
            count += 1
    return count
        
def flipper(str_num, mapper):
    if str_num in mapper:
        return mapper[str_num]
    else:
        if len(str_num) < 2:
            return None
        flipped = []
        for i in [*str_num]:
            if mapper.get(i):
                flipped.append(mapper[i])
            else:
                return None
        return ''.join(flipped)[::-1]