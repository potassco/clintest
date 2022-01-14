class NotCallable(Exception):
        def __init__(sel, message='Object passed is not callable'):
            super().__init__(message)


class TestCaller:
    def __init__(self,name, call):
        if callable(call):
            self.call = call
            self.name = name
        else:
            raise NotCallable
    
    def __call__(self,MR,args):
        return self.call(MR,args)


def func_sat(mr,arg):
    if mr.models:
        return True and arg, None
    else :
        return False and arg, None

def func_trueinall(mr,arg):
    if not isinstance(arg, set):
        atoms = set(arg)

    ret = True
    info = ""
    models = mr.models

    for m,i in zip(models,range(len(models))):
        m = set(m)
        if not atoms.issubset(m):
            ret = False
            info += f'\n    -\tMissing symbol(s) on model {i} : '
            for s in arg:
                if not s in m:
                    info += s + ' '
                
    return ret,info
    



listTC = [
    TestCaller('sat', func_sat),
    TestCaller('trueinall', func_trueinall)
]
