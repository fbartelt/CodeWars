class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.key = key
        self.alphabet = alphabet
    def encode(self, text):
        b = ''.join([self.key[i%len(self.key)] for i in range(len(self.alphabet))])
        print(b,len(b),len(self.alphabet))
        return ''.join([b[self.alphabet.index(x)] if x in self.alphabet else x for x in text])

    def decode(self, text):
        pass


code = "pass"
alp = "abcdefghi"
b = ''.join([code[i%4] for i in range(len(alp))])
msg = "bac"
print(b)
cip = [b[alp.index(x)] for x in msg]
print(cip)

abc = "abcdefghijklmnopqrstuvwxyz"
key = "password"
msg = "codewars"
b = ''.join([key[i%len(key)] for i in range(len(msg))])
print(b)
k = ''.join([abc[((key[x])-msg[x])%26] if msg[x] in abc else msg[x] for x in range(len(msg))])
print(key[1])
print(k)
c = VigenereCipher(key, abc)
c.encode("codewars")

[x if x in key if (x in abc and 1 )+ x]
