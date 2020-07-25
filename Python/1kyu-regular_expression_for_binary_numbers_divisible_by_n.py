def regex_divisible_by(n):
    ## PRA REGEX: percorrer dfa ao contrario e ir substituindo as keys?
    dfa = get_dfa(n)
    for states in list(dfa.keys())[::-1]:
        print(dfa[states])

def get_dfa(n):
    ACCEPTING_STATE = START_STATE = '0'
    SYMBOL_0 = '0'
    dfa = {
        str(states):{
            str(symbol): 'to_state' for symbol in range(2)
        }
        for states in range(n)
    }
    print(dfa)
    dfa[START_STATE][SYMBOL_0] = ACCEPTING_STATE
    # `lookup_table` keeps track: 'number string' -->[dfa]--> 'end_state'
    #lookup_table = { SYMBOL_0: ACCEPTING_STATE }.setdefault
    lo = [str(a // 2) for a in range(2 * n)]
    print(lo)
    for num in range(2 * n):
        end_state = str(num % n)
        binary = bin(num)
        before_end_state = lo[num]
        print(lo[num], binary, end_state)
        dfa[before_end_state][binary[-1]] = end_state
        print(dfa)
        #lookup_table(num_s, end_state)
    print(dfa)
    return dfa

regex_divisible_by(5)