def regex_divisible_by(n):
    if n==1:
        return '^(0|1)+$'
    dfa = get_dfa(n)
    while len(dfa) > 2:
        current_state = list(dfa)[-1]
        current_transitions = get_self_state(current_state, dfa[current_state])
        dfa.pop(current_state,None)
        for _, transitions in dfa.items():
            if (current_state in transitions.keys()):
                change_states(transitions, current_transitions, current_state)
        dfa.pop(current_state,None)
    state_one = list(dfa)[-1]
    state_one = get_self_state(state_one, dfa[state_one])
    regex = '^(?:0|1{})+$'.format(state_one['0'])
    return regex

def change_states(transitions, current_transitions, current_state):
    holded = 0
    middle = transitions[current_state]
    for to_state, value in current_transitions.items():
        if (to_state in transitions.keys()):
            transitions[to_state] = '(?:{}|{}{})'.format(transitions.pop(to_state),middle ,value)
        else:
            value_hold = transitions.pop(current_state, '')
            if value_hold != '':
                holded = value_hold
            value_ = '{}{}'.format(holded or value_hold, value)
            transitions.setdefault(to_state, value_)
    return transitions

def get_self_state(state, to_states):
    dicio = {}
    self_state = ''
    for key, value in to_states.items():
        if key == state:
            self_state = '(?:{})*'.format(value)
        else:
            dicio.setdefault(key, value)
    dicio = {key : self_state+value for key,value in dicio.items()}
    return dicio

def get_dfa(n):
    ACCEPTING_STATE = START_STATE = '0'
    SYMBOL_0 = '0'
    dfa = {
        str(states):{}
        for states in range(n)
    }
    dfa[SYMBOL_0].setdefault(ACCEPTING_STATE,START_STATE)
    lo = [str(a // 2) for a in range(2 * n)]
    for num in range(2 * n):
        end_state = str(num % n)
        binary = bin(num)
        before_end_state = lo[num]
        dfa[before_end_state].setdefault(end_state,binary[-1])
    return dfa

##### TEST FUNCTION
import re
def check_func(n):
    for i in range(1,n):
        pattern = re.compile(regex_divisible_by(i))
        lista = [x for x in range(1000) if not x%i ]
        lista2 = [x for x in range(1000) if re.search(pattern, bin(x)[2:])]
        print('PAT', pattern)
        if lista == lista2:
            print(i, 'OK')
        else:
            print(i, 'BAD')
#check_func(19)
print(regex_divisible_by(11))
