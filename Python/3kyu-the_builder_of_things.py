def add_method(cls):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)   
        print(func.__name__) 
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator

class Thing (object):
    def __init__(self, name):
        self.name = name
    def __getattr__(self, test):
        print('cal', callable(test))
        print('aqui porra', test, test.__class__)
        setattr(Thing, test, 3)
        #print(Thing.__getattr__(self,macaco))
    def __get__(self, instance, owner):
        print ("returned from descriptor object")
        print(instance, owner)
        return self.value
a = Thing('JOn')
@add_method(Thing)
def foo(s):
    print('aaa'+s)
    return 3

b= a.kakaka_test_2_quatro
b = a.kakaka_test_2_quatro.ll
#print(a.__getattribute__('kakaka_test_2_quatro.ll'))
#a.foo()
 
        