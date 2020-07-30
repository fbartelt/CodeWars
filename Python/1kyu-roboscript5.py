import re
from collections import deque
class RSUProgram:
    def __init__(self, source):
        self.source = source
        self.possible_recs = set([])
    def get_tokens(self):
        clean_source = self.tidy_up()
        full_token = ''
        token_list = []
        for token in clean_source:
            if token.isdigit():
                full_token += token
            else:
                if full_token:
                    token_list.append(full_token)
                    full_token = token
                else:
                    full_token += token
        token_list.append(full_token)
        #print(token_list)
        self.tokens = token_list
        return token_list
    def tidy_up(self):
        # se nao tiver funcionando: (?:^|\n) isso no começo talvez resolva
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
        print(no_space)
        stray_comments = re.search(r'(\*\/)|(\/\*)', no_space)
        if stray_comments:
            raise SyntaxError('Stray comments in  => ' + stray_comments[0])
        self.clean = no_space
        return no_space
        
    def convert_to_raw(self, tokens):
        #### RECURSAO TA SENDO MESMO SE O CÓDIGO RODADO NAO GERA ISSO. É PRA DAR RAISE SÓ NO CASO DE RODAR
        ####    TEST #4
        #### ARRUMADO COM UMA GORILADA, TALVEZ QUEBRE EM BREVE
        raw = []
        patterns = {}
        scope = [patterns]
        commands_stack = []
        labels = []
        post_operations = 0
        pattern_bracket = re.search(r'(\(.*?p.*?q\))|(\([\)]*?q[\(]*?\))', self.clean)
        ### SE NAO TIVER PERFEITO: (\([^\)]*?p[^\(]*?.*?\))|(\([^\)]*?q[^\(]*?\))
        if pattern_bracket:
            raise SyntaxError('Nesting pattern definitions within bracketed sequences => '+pattern_bracket[0])
        for token in tokens:
            if 'p' in token:
                label = token[1:]
                labels.append(label)
                if label in scope[-1].keys():
                    raise SyntaxError('Pattern ' + token + ' already definided in current scope')
                scope[-1].update({label: {}})
                scope.append(scope[-1][label])
                commands_stack.append(token)
                post_operations += 1
            #na hora do 'q' talvez dê pra dar o scope[-1].uptade({label: comands})
            elif token == 'q':
                if len(scope) <= 1:
                    raise SyntaxError('Number of patterns defined does not match with number of endings')
                cmd = commands_stack.pop()
                pattern_definition = []
                if 'p' in cmd:
                    pattern_definition.append('')
                while 'p' not in cmd:
                    if 'P' in cmd:
                        label_ = cmd[1:]
                        translated = self.translate_patterns([cmd], scope, 1)
                        if cmd in self.possible_recs: self.possible_recs.remove(cmd)
                        pattern_definition.extend(translated[::-1])
                    else:
                        pattern_definition.extend(cmd)
                    cmd = commands_stack.pop()
                scope.pop()
                ### TIREI O [::-1] DO PATTERN_DEFIINITION PRA TENTAR DESINVETER
                scope[-1].update({labels.pop() : pattern_definition[::-1]})
                post_operations -= 1
            #######
            # k = list(dict(x) for x in b)
            ####### jeito certo pra copiar o scope sem ficar mudando
            elif 'P' in token:
                #possible_scopes = list(dict(x) for x in scope)
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
                    ### TIREI O [::-1] DO CMD_SEQUENCE PRA TENTAR DESINVETER
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
        self.patterns = patterns
        raw = self.translate_patterns(raw, scope)
        return raw

    def translate_patterns(self, raw, scope,local=0, loop=0, not_exec_recursion = []):
        final_raw = []
        #print(self.possible_recs)
        #print('LOOP',loop, local, not_exec_recursion)
        #print(any(x in raw for x in self.possible_recs))
        #print(raw)
        if loop>10 and local:
            #print('\n\nCHEGO\n\n')
            self.possible_recs |= set(not_exec_recursion)
            #return not_exec_recursion[-1]
        if (loop>15 and any(x in self.possible_recs for x in raw)) or loop>130:
            raise RecursionError('Maximum recursion depth exceeded')
        for token in raw:
            if 'P' in token:
                label_ = token[1:]
                for i, definitions in enumerate(scope[local:][::-1]):
                    if label_ in definitions.keys() and definitions[label_]:
                        self.possible_recs |= set([token])
                        definition = definitions[label_]
                        final_raw.extend(self.translate_patterns(definition, scope, local, loop+1))
                        break
                    elif i == len(scope)-local-1:
                        if local:
                            final_raw.append(token)
                        else:
                            raise NameError('Pattern "p' +label_+  '" not defined in this scope')
            else:
                final_raw.append(token)
        return final_raw
       
    def execute_raw(self, cmds):
        pos, directions = (0,0), deque([(1,0),(0,-1),(-1,0),(0,1)])
        passed_by = {pos}
        #print('cmdds', self.clean)
        for cmd in cmds:
            if cmd == 'F':
                pos = tuple(pos_0+pos_f for pos_0, pos_f in zip(pos,directions[0]))
                passed_by.add(pos)
            elif cmd in ['L','R']:
                directions.rotate((-1)**(cmd=='R'))
        minX, maxX = min(x for x,y in passed_by), max(x for x,y in passed_by)
        minY, maxY = min(y for x,y in passed_by), max(y for x,y in passed_by)
        string='\r\n'.join(''.join('*' if (x,y) in passed_by else ' 'for x in range(minX, maxX+1)) for y in range(maxY,minY-1,-1))
        return string
    def execute(self):
        a = self.convert_to_raw(self.get_tokens())
        print(self.patterns)
        return self.execute_raw(a)

#test = RSUProgram('/*some nosense here and there*//**/ /*hehye*/p0\n  (\n    F2L\n  )2 (\n    F2 R\n  )2\nq\n//HELLO FUCKERS\n(\n  P0\n)2')
#test = RSUProgram('p3\n  RR(\n    F4 L\n  )4\nq\n\nP3(FL)2RRF')
#test = RSUProgram('p0(RR)2qp1LLLP0qp3FFFFP1qRRP3')
#4\/
#test = RSUProgram('p0((((F2LF3R)2))2)2qp1F3P1F2qp2FLP3FRqp3FRP2FLqp4p1F3P1F2qp2FLP3FRqp3FRP2FLqLP1RP2LP3Rqp5F5(P16)5L2qP0')
# failing test 
# V
#test = RSUProgram('RP372RL8FF(P372(()1R1F)F3F)P428(F7)4(LF8(P372P372R2)1F3)7p3p372RLL6P914p372F7R5F4L2R()qF6FL9FqqLR4L8(R6LR7)3FRp372p477L2FFFP914P914(L5F4)6R1R7qP477F8F5RqLP372R6RL1RFP3F5P3LRF2RF7LP428FFRP372P372p914R4F1p707F1qRL(R1R2)qR2L6FFp428p7R2p152P7LP152p7qqp707LF()9L9R0qP152p12FR6F9P5R6()3p477qp5qqqp914F2LFFR8qp12R2F6RL(()F)7R0R0L7qP7L4RFFq')
#test = RSUProgram('RR6(L0RL2)P186F6F8(LFLF7)0FP186L7L5p9R5P9LFF5R5p9F8LqqR7p186p8p529p511qp424qp728qF4R()Fqp9R()FLR2F9L7P728P186()3qqp850LFL6qFRF8P728(LP9LL8)2p728p850L()4()0P728FLP468P468LFL9p468P850qqFP8F(FL6R)5FF0LL8P850F1R5L9Lqq')
#test = RSUProgram('p1FFqp0RRRp1FFFqqP0')
#test = RSUProgram('F9P833R4RRP499P188LL5p833LRRR6LF0FRR5Rp680P242F8RqqF4RFP7L(RRF9F)R5p176R4LL4R3FR4p242P7LF7R5LFRp397q*/LLRp499p4qRqL1RL1(())FRFF9qFRqP499F6p499RP833LR2F1P242R0F5R9P176LFqF1L9R7LF(R5)L2FR5R1((F(LR3)F0)FF6R)(P3L6)F6p188Lqp647P833Fq(R3)L0P499Fp242p499LL7L5qqF1F8P188p7LR4qP242P833L4LP188(P833F)LRL4F9R3F3RR1L1p3LFF1R0LR2P176L0p647P499F8RP176F3LFL6p470RF0()8FqR6(L9LRF5)7R4R5F0qq')
#test = RSUProgram('p0RR1(F)(FP769FL0)L5R4LP215R1R(P215)1RP867qL9(R)9(P769)6F2P0(L1F7)(FP769)F2p408p0P658RP888F8qL1p408p0L()7()RL2p8qqR7R(R0RRP867)8F(FP867)L5FL6FqqL4LF5Fp888p867p5F3RLFp5qp658qLP769()F9R1L6()qp698LL3p869qL9RFP867L8RR9F3F7q(RLL2)LR(F5LP698)F5P408LqP867P867FF2L9R8P408R2F1qp867R1L8R0F1RqRL9R5F3(R6P769F4)4F3R9p5FL6P215F1L(L7F2FR)3P408p215p317R9()R5LL8()R8L0F7F7Fp204qqL2LRqLL(L5F4FR)5qp215F0F2F9RFR2L5p698p693RRRR0()qqL(P888LL9F(R3P5()P408R1)2)F6L8F(P867R)3R2P408qL4F(R((R7F8()P215)4R0)LF9)0RRFp658RR3FL0p693R1L1LF3(P3F3)p3RP658()qqp658L1p190L7RR2L()Lqqp530LF9P408L7FP769(()8L0())qFqFL7LP658F0F8RP888(L)R6P867F7L3(L4F4)RFRP658L0P769L9R3(P408F)LP769P5Rp769F0p769(FR8)(FRR)LRLL3RLRR8R4L7(F3LR7L1)p429R3P658L6L6qLP429Rq((F7)4(LFFR6)7)FP215P867L4(F4(F9F3F7)8F5P215)6F0LqFLR2(R6FRRF8)6FL2P0')
###### TESTAR NESSES VVVVV

test = RSUProgram('p420L7FR7(LR(LP663))8P1RP1(F1FR)9R2F9FP906F8p906p798LR3P906Lp669qq(R8RLLF1)(P880R9()LL4)0RqqF2()R(R6)p669FF6P1F3(P880)9FF7RLR8FL7qP669(P669)FRLP2RFF9LP2F4p6L0FFLR5P880R3(F5(R1LL5F4)P880(F)F0)LP358Fqp1P258()6F(LL8R(F5F0))p258FRFRL3F9FP6(FR()L4)9R(FF8P6P880R)F3FLP880LqqF9p880p420RL0F1L1p139()p1qP880()P669LL4()0qqp1R7F9F7p669FLLp164qL()0F()5FqqLF3FF9(F5P1R2F)9F((()()0)3)5qp663LF7L6LF7P669P880(FFR3)2(RR9F)(P358R3L4)RF2Lqp2p386p149P2LLLp880qL0F8F8RRRP1qp880F6F7RP6qL0R4RL2Lqp469P2p604()P819R5P880P2RP1F4FRqp2L7p4qP604F3LL8R8R3F5()Fqp819()()Rp963qP6LqqF6R(RR9)F5P358P469(F4L(()6L))L0Rq(FRF5)FRP420LF4RL0p358P880P880R1R7qL7(L0L6R8F2F0)4LLL9(RFFR8)0')
#test = RSUProgram('R4p109p109LRL3FL5qp20L3P171L0L6FLLqp910p164LR4R3RL4()3R5R9R()0()5F()6qq(LL2R6R7)FqF5p20P544(R6F1P171)7FLRP544FL(R2R9)5(R3)5Lp301p376LP7F3R()qRRF3p301F7F1()P910L0F7()7RFF1qp910LFR9L3qp7P109F2L2LR3R1()qqqp910F5L6F0p171F0LqRRLR1p560R(FP20)4(L6)F0F4qp715RFFRR6(L9LP109R)p715FRP109()9RR6LR7qqqp171FFP544FL1qP910RR5L7p715p544(P171R)Fp252p307qF8()F4qF0FF9RqRF0FL(F)5RP171RqF9FFP715P20L1RP171R8RRR8R8F4R7p544P109F3R5RR3qR7(R6RR(LP910(P171)F8)8)7R8RR1P20L7FF')

# p1p3FLqp4FP3qFP4qp2F3Rq(P1P2)2
# P3 = FL, P4 = FFL, P2 = FFFR, P1 = FFFL
#a = test.get_tokens()
a= test.execute()
print(test.possible_recs)
#print(test.tokens)
#b=test.convert_to_raw(a)
#test.execute_raw(b)
#print(test.patterns,len(test.patterns))
#print([(x,len(y)) for x,y in test.patterns.items()])
#print(test.patterns)
#print(test.possible_recs)

#test.tidy_up()

## ['p0', '(', 'F2', 'L', ')2', '(', 'F2', 'R', ')2', 'q', '(', 'P0', ')2']
## ['p3', 'R', 'R', '(', 'F4', 'L', ')4', 'q', 'P3', '(', 'F', 'L', ')2', 'R', 'R', 'F']
## FFFFLLLRRRR


### old func when token 'p'
""" elif 'P' in token:
                print('cheguei')
                label_ = token[1:]
                popped = 0
                if any('p' in c for c in commands_stack):
                    popped = 1
                    aux = scope.pop()
                if label_ not in scope[-1].keys():
                    raise NameError('Trying to call "'+ token+ '" but pattern "p' + label_ + '" was not defined in this scope')
                elif post_operations:
                    print('aqui')
                    ## TIREI O [::-1] DO FINAL DO ARGUMENTO DOS DOIS APPENDS ABAIXO
                    commands_stack.append(scope[-1][label_])
                else:
                    raw.append(scope[-1][label_])
                if popped:
                    scope.append(aux) """


### OLD TRANSLATE_PATTERN

""" idx = 0
        while any(type(x) == tuple for x in raw):
            if loop > 50:
                raise ValueError('Possible infinite loop')
            #print(idx)
            token = raw[idx]
            #print(token)
            if type(token) == tuple:
                pattern = raw.pop(idx)
                label = pattern[0]
                definitions = pattern[1]
                for i, definition in enumerate(definitions[::-1]):
                    if label in definition.keys():
                        #print('def',definition[label])
                        raw[idx:idx] = self.translate_patterns(definition[label], loop+1)
                    elif i == len(definitions)-1:
                        raise NameError('Pattern "p' +label+  '" not defined in this scope')
            else:
                print('yay')
            #print('raw',raw)
            #print('fnial', final_raw)
            idx += 1
        return raw """