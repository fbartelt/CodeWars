
def create_phone_number(n):
    zapzap = ("("+''.join(str(n[x]) for x in range(3)) + ")") + (" " +
    ''.join(str(n[x]) for x in range(3,6)) + "-") + (''.join(str(n[x]) for x in range(6,10)))
    print (zapzap)
    return zapzap

create_phone_number([1,2,3,4,5,6,7,8,9,0])
