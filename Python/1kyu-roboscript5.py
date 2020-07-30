import re
from collections import deque

class RSUProgram:
    def __init__(self, source):
        self.source = source

    def get_tokens(self):
        self.tidy_up()
        full_token = ''
        token_list = []
        for token in self.clean:
            if token.isdigit():
                full_token += token
            else:
                if full_token:
                    token_list.append(full_token)
                    full_token = token
                else:
                    full_token += token
        token_list.append(full_token)
        return token_list

    def tidy_up(self):
        bad_comment = re.search(r'((?:\)|[pFLRP])[0-9]*((\/\*.*\n*.*\*\/)+|\/\/.*\n+)[0-9]+)+', self.source)
        if bad_comment:
            raise SystemError('Invalid comment within token in => '+ bad_comment[0])
        no_comments = re.sub(r'(\/\*(?:\n|.)*?\*\/)|(?:(\/\/.*)(?:\n|$))', '', self.source)
        space_token_err = re.search(r'((?:\)|[pFLRP])\s+[0-9]+)+|([a-or-zA-EG-KM-OQS-Z])', no_comments)
        if space_token_err:
            raise SyntaxError('Invalid Tokens or whitespace within tokens in => '+ space_token_err[0])
        no_space = re.sub(r'\s+', '',no_comments)
        pattern_zeros_err = re.search(r'(p|P)([^0-9]|$)|([FRLPp)]0[0-9]+)', no_space)
        if pattern_zeros_err:
            raise SyntaxError('Leading zeros or non-identified pattern in => ' + pattern_zeros_err[0])
        stray_comments = re.search(r'(\*\/)|(\/\*)', no_space)
        if stray_comments:
            raise SyntaxError('Stray comments in  => ' + stray_comments[0])
        self.clean = no_space
        
    def convert_to_raw(self, tokens = None):
        if not tokens: tokens = self.get_tokens()
        raw = []
        patterns = {}
        scope = [patterns]
        commands_stack = []
        post_operations = 0
        pattern_bracket = re.search(r'(\(.*?p.*?q\))|(\([\)]*?q[\(]*?\))', self.clean)
        if pattern_bracket:
            raise SyntaxError('Nesting pattern definitions within bracketed sequences => '+pattern_bracket[0])
        for token in tokens:
            if 'p' in token:
                label = token[1:]
                if label in scope[-1].keys():
                    raise SyntaxError('Pattern ' + token + ' already definided in current scope')
                scope[-1].update({label: {}})
                scope.append(scope[-1][label])
                commands_stack.append(token)
                post_operations += 1
            elif token == 'q':
                if len(scope) <= 1:
                    raise SyntaxError('Number of patterns defined does not match with number of endings')
                cmd = commands_stack.pop()
                pattern_definition = []
                if 'p' in cmd: pattern_definition.append('')
                while 'p' not in cmd:
                    pattern_definition.append(cmd) if 'P' in cmd else pattern_definition.extend(cmd)
                    cmd = commands_stack.pop()
                scope[-1].update({'00' : pattern_definition[::-1]})
                scope.pop()
                post_operations -= 1
            elif 'P' in token:
                if post_operations:
                    commands_stack.append(token)
                else:
                    raw.append(token)
            elif token == '(':
                commands_stack.append(token)
                post_operations += 1
            elif ')' in token:
                multiplier = int(token[1:]) if token[1:] else 1
                cmd = commands_stack.pop()
                cmd_sequence = []
                while cmd != '(':
                    if any(c in ['p','q'] for c in cmd):
                        raise SyntaxError('Nesting pattern definitions within bracketed sequences => '+cmd)
                    if 'P' in cmd:
                        cmd_sequence.append(cmd)
                    else:    
                        cmd_sequence.extend(cmd)
                    cmd = commands_stack.pop()
                post_operations -= 1
                if post_operations:
                    commands_stack.extend(cmd_sequence[::-1]*multiplier)
                else:
                    raw.extend(cmd_sequence[::-1]*multiplier)
            else:
                multiplier = token[1:]
                cmd = token[0] * int(multiplier) if multiplier else token
                if post_operations:
                    commands_stack.extend(cmd)
                else:
                    raw.extend(cmd)
        if post_operations !=0:
            raise SyntaxError('Unmatching parenthesis or pattern definitions/ending')
        return self.translate_patterns(raw, [patterns])

    def translate_patterns(self, raw, pattern_list, loop=0):
        final_raw = []
        if loop>20 :
            raise RecursionError('Maximum recursion depth exceeded')
        for token in raw:
            if 'P' in token:
                label_ = token[1:]
                err = 1
                for iters, patterns in enumerate(pattern_list[::-1]):
                    if label_ in patterns.keys():
                        local_pattern = patterns[label_] 
                        definition = local_pattern['00']
                        _pattern_list = pattern_list[:len(pattern_list)-iters] + [local_pattern]
                        final_raw.extend(self.translate_patterns(definition, _pattern_list, loop+1))
                        err = 0
                        break
                if err: raise NameError('Pattern "p' + label_ + '" not defined in this scope')
            else:
                final_raw.append(token)
        return final_raw
       
    def execute_raw(self, cmds = None):
        if not cmds: cmds = self.convert_to_raw()
        pos, directions = (0,0), deque([(1,0),(0,-1),(-1,0),(0,1)])
        passed_by = {pos}
        for cmd in cmds:
            if cmd == 'F':
                pos = tuple(pos_0 + pos_f for pos_0, pos_f in zip(pos,directions[0]))
                passed_by.add(pos)
            elif cmd in ['L','R']:
                directions.rotate((-1)**(cmd=='R'))
        minX, maxX = min(x for x,y in passed_by), max(x for x,y in passed_by)
        minY, maxY = min(y for x,y in passed_by), max(y for x,y in passed_by)
        string = '\r\n'.join(''.join('*' if (x,y) in passed_by else ' 'for x in range(minX, maxX+1)) for y in range(maxY,minY-1,-1))
        return string

    def execute(self):
        return self.execute_raw()

#test = RSUProgram('/*some nosense here and there*//**/ /*hehye*/p0\n  (\n    F2L\n  )2 (\n    F2 R\n  )2\nq\n//HELLO FUCKERS\n(\n  P0\n)2')
#test = RSUProgram('p0((((F2LF3R)2))2)2qp1F3P1F2qp2FLP3FRqp3FRP2FLqp4p1F3P1F2qp2FLP3FRqp3FRP2FLqLP1RP2LP3Rqp5F5(P16)5L2qP0')

#INFINITE RECURSION
#test = RSUProgram('RP372RL8FF(P372(()1R1F)F3F)P428(F7)4(LF8(P372P372R2)1F3)7p3p372RLL6P914p372F7R5F4L2R()qF6FL9FqqLR4L8(R6LR7)3FRp372p477L2FFFP914P914(L5F4)6R1R7qP477F8F5RqLP372R6RL1RFP3F5P3LRF2RF7LP428FFRP372P372p914R4F1p707F1qRL(R1R2)qR2L6FFp428p7R2p152P7LP152p7qqp707LF()9L9R0qP152p12FR6F9P5R6()3p477qp5qqqp914F2LFFR8qp12R2F6RL(()F)7R0R0L7qP7L4RFFq')

#STRAY COMMENT
#test = RSUProgram('F9P833R4RRP499P188LL5p833LRRR6LF0FRR5Rp680P242F8RqqF4RFP7L(RRF9F)R5p176R4LL4R3FR4p242P7LF7R5LFRp397q*/LLRp499p4qRqL1RL1(())FRFF9qFRqP499F6p499RP833LR2F1P242R0F5R9P176LFqF1L9R7LF(R5)L2FR5R1((F(LR3)F0)FF6R)(P3L6)F6p188Lqp647P833Fq(R3)L0P499Fp242p499LL7L5qqF1F8P188p7LR4qP242P833L4LP188(P833F)LRL4F9R3F3RR1L1p3LFF1R0LR2P176L0p647P499F8RP176F3LFL6p470RF0()8FqR6(L9LRF5)7R4R5F0qq')

#INFINTE RECURSION BUT NOT IN EXECUTION
test = RSUProgram('R4p109p109LRL3FL5qp20L3P171L0L6FLLqp910p164LR4R3RL4()3R5R9R()0()5F()6qq(LL2R6R7)FqF5p20P544(R6F1P171)7FLRP544FL(R2R9)5(R3)5Lp301p376LP7F3R()qRRF3p301F7F1()P910L0F7()7RFF1qp910LFR9L3qp7P109F2L2LR3R1()qqqp910F5L6F0p171F0LqRRLR1p560R(FP20)4(L6)F0F4qp715RFFRR6(L9LP109R)p715FRP109()9RR6LR7qqqp171FFP544FL1qP910RR5L7p715p544(P171R)Fp252p307qF8()F4qF0FF9RqRF0FL(F)5RP171RqF9FFP715P20L1RP171R8RRR8R8F4R7p544P109F3R5RR3qR7(R6RR(LP910(P171)F8)8)7R8RR1P20L7FF')
tt = test.execute()
print(tt)
