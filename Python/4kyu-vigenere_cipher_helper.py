class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.key = key
        self.alphabet = alphabet
    def encode(self, text):
        encoded = ''
        for idx, char in enumerate(text):
            if char in self.alphabet:
                char_pos = self.alphabet.index(char)
                key_pos = self.alphabet.index(self.key[idx % len(self.key)])
                encoded += self.alphabet[((char_pos + key_pos) %len(self.alphabet))]
            else:
                encoded += char
        return encoded
    def decode(self, text):
        decoded = ''
        for idx, char in enumerate(text):
            if char in self.alphabet:
                char_pos = self.alphabet.index(char)
                key_pos = self.alphabet.index(self.key[idx % len(self.key)])
                decoded += self.alphabet[((char_pos - key_pos) %len(self.alphabet))]
            else:
                decoded += char
        return decoded

abc = "abcdefghijklmnopqrstuvwxyz"
key = "password"
msg = "codewars"

c = VigenereCipher(key, abc)
print('aaa')
a = c.encode('codewars C')
print(a)

#[x if x in key if (x in abc and 1 )+ x]
