import itertools
def switch(argument):
    switcher = {
        'F': "pink",
        'L': "red",
        'R': "green",
        '0' : "orange",
        '1' : "orange",
        '2' : "orange",
        '3' : "orange",
        '4' : "orange",
        '5' : "orange",
        '6' : "orange",
        '7' : "orange",
        '8' : "orange",
        '9' : "orange"
    }
    return switcher.get(argument, '')

def highlight(code):
    err = ['(',')']
    prev = ''
    x=-1
    l1 = []
    l2 = []
    for indice in code:
        if(prev == indice or (prev.isdecimal() and indice.isdecimal())):
            l1[x].append(indice)
        else:
            x+=1
            l1.append([indice])
        prev = indice
    for indice in l1:
        if indice[0] in err:
            l2.append(indice)
        else:
            l2.append("<span style=\"color: "+switch(indice[0])+"\">")
            l2.append(indice+["</span>"])
    return ''.join(list(itertools.chain.from_iterable(l2)))
