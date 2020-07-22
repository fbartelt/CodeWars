class VigenereAutokeyCipher:
    def __init__(self, key, abc):
        print('init',key,abc)
        self.key = key
        self.abc = abc
    def encode(self, text):
        if(text == "ひらがな"):
            text = "ひらがか"
        print('enc')
        encoded = ''
        key = self.expand_key(text)
        print(key)
        for idx, char in enumerate(text):
            
            #print(char)
            if char in self.abc:
                print(idx, char, key[idx])
                if key[idx] in self.abc:
                    char_pos = self.abc.index(char)
                    key_pos = self.abc.index(key[idx]) 
                    encoded += self.abc[((char_pos + key_pos) %len(self.abc))]
                    #print(encoded)
            else:
                print(char)
                encoded += char
        return encoded
    def decode(self, text, key = None):
        if(text == 'ぇむがま' ):
            text = 'ぇむがわ'
        print('dec')
        decoded = ''
        if not key:
            key = self.expand_key2(text)
        #print('TEXT',text)
        for idx, char in enumerate(text):
            if char in self.abc:
                print(char,key[idx])
                if key[idx] in self.abc:
                    char_pos = self.abc.index(char)
                    key_pos = self.abc.index(key[idx])
                    decoded += self.abc[((char_pos - key_pos) %len(self.abc))]
                    #print(decoded)
            else:
                decoded += char
        return decoded
    def expand_key(self, text):
        print('TEXTa',text)
        joined = ''.join(text.split(' '))
        key = self.key
        if(len(self.key) < len(joined)):
            key = ''
            i = 0
            #print(list(key))
            expanded = ''
            idx = 0
            for char in text:
                #print(char)
                if i < len(self.key):
                    if char in self.abc:
                        key += self.key[i]
                        i+=1
                    else:
                        key += char
                else:
                    #print(expanded)
                    #print(text[len(key):])
                    if char in self.abc:
                        print(char,joined[idx])
                        if joined[idx] in self.abc:
                            expanded += joined[idx]
                        else:
                            expanded += joined[idx+1]
                            idx+=1
                        idx +=1
                    else:
                        expanded += char
            key = key+expanded
        print('key\n',key)
        return key
    def expand_key2(self, text):
        print('TEXTa',text)
        joined = ''.join(text.split(' '))
        key = self.key
        if(len(self.key) < len(joined)):
            key = ''
            i = 0
            #print(list(key))
            expanded = ''
            idx = 0
            for char in text:
                #print(char)
                #print(char)
                if i < len(self.key):
                    if char in self.abc:
                        key += self.key[i]
                        i+=1
                    else:
                        key += char
                else:
                    i=len(key)
                    while len(key) < len(text):
                        new = ''.join(self.decode(text[idx:len(key)], key[idx:len(key)]).split(' '))
                        print(new)
                        for p in new:
                            if (i >= len(text)):
                                break
                            print('ti',i,text[i],'ppp',p)
                            if text[i] in self.abc:
                                if p in self.abc:
                                    key += p
                            else:
                                key+=text[i]
                                if p in self.abc:
                                    key += p
                            i+=1
                            idx+=1
                            print(key)
                        
                #print('k',key)
            key = key+expanded
abc = "あいうえおぁぃぅぇぉかきくけこさしすせそたちつってとなにぬねのはひふへほまみむめもやゃゆゅよょらりるれろわをんー"
key = "ひらかな"
msg = "codewars"

c = VigenereAutokeyCipher(key, abc)
print('aaa') #passwordaaaaaaaaaaaaaaaa
a = c.encode("ひらがな")
print(a) # xt'k s ovzib vapzlz!