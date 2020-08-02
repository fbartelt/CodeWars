def runShell(boxNr):
    print (boxNr)
    if boxNr == 1:
        return "cd /root ; ls ; echo root.txt ; CodeWars{7594357083475890320019dsfsdjfl32423hjkasd9834haksdSKJAHD32423khdf}"
    elif boxNr == 2:
        return "cd /etc; ls -l; cat passwd;echo root:$1$root$quimBCDAqK3JX3mbeqrrD1:0:0::/root:/bin/bash > passwd; su root pass123; cd /root; ls -l; cat root.txt; CodeWars{jfklsfjljlk&8632847dhfkjds876fDKJFHD(F&/KHKJDF}"
        # openssl passwd -1 -salt root pass123
    else:
        return "help ; pwd; ls -la ; whoami; cat .hidden_password_for_root.txt; cat root.txt fil3pa44word; CodeWars{fdjslfd2433SKAJF(/&Dfkhk3h4kfsd786234kjf}"
        # convert .hidden...txt into list of list of bits(21) using code below and make it a QRcode
        # decode QRcode with https://zxing.org/w/decode ==> fil3pa44word;
    

thing = 'black;black;black;black;black;black;black;white;white;white;black;white;black;white;black;black;black;black;black;black;black;\
black;white;white;white;white;white;black;white;black;white;black;white;black;white;black;white;white;white;white;white;black;\
black;white;black;black;black;white;black;white;black;white;black;black;white;white;black;white;black;black;black;white;black;\
black;white;black;black;black;white;black;white;white;white;white;white;black;white;black;white;black;black;black;white;black;\
black;white;black;black;black;white;black;white;black;black;black;white;black;white;black;white;black;black;black;white;black;\
black;white;white;white;white;white;black;white;black;black;black;white;white;white;black;white;white;white;white;white;black;\
black;black;black;black;black;black;black;white;black;white;black;white;black;white;black;black;black;black;black;black;black;\
white;white;white;white;white;white;white;white;black;white;white;black;white;white;white;white;white;white;white;white;white;\
black;black;white;black;white;white;black;black;white;white;black;black;black;white;black;black;black;white;black;black;white;\
black;white;black;white;white;black;white;white;black;black;black;black;white;black;white;white;white;white;white;black;white;\
white;white;white;black;black;white;black;black;white;white;black;black;black;white;white;white;white;white;white;white;white;\
black;black;black;black;black;white;white;black;white;white;white;white;black;white;black;black;black;black;white;black;black;\
white;white;black;white;white;white;black;white;white;white;black;black;black;white;black;black;black;white;white;white;black;\
white;white;white;white;white;white;white;white;black;white;black;black;black;white;white;black;black;white;white;white;white;\
black;black;black;black;black;black;black;white;black;black;black;black;black;black;black;white;black;black;white;black;white;\
black;white;white;white;white;white;black;white;white;white;black;white;black;white;white;white;black;black;black;black;black;\
black;white;black;black;black;white;black;white;white;white;black;black;black;black;black;black;white;black;black;black;white;\
black;white;black;black;black;white;black;white;black;black;white;black;black;white;black;white;black;black;white;white;black;\
black;white;black;black;black;white;black;white;white;black;white;black;white;black;white;white;black;white;white;white;black;\
black;white;white;white;white;white;black;white;black;black;white;black;black;black;white;white;white;white;black;black;black;\
black;black;black;black;black;black;black;white;black;black;black;white;black;black;black;white;black;black;black;black;white;'
test = [[]]
lista = thing.split(';')
lista.pop()
for bit in lista:
    test[-1].append(str(int(bit == 'black')))
    if len(test[-1]) == 21:
        test.append([])
print('\n'.join(''.join(x for x in bits)  for bits in test))

