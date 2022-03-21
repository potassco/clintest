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
    

def func_modelcost(mr,arg):
    if type(arg) == type([]):
        cost = arg
    else :
        cost = [arg]

    if len(cost) != len(mr.cost) and len(mr.cost) > 0:
        return False,f'Cost informations differ in size : found {cost}, waited {mr.cost}'

    ret = True 
    info = ""
    for c ,i in zip(mr.cost,range(len(mr.models))):
        if c !=cost[i]:
            ret = False
            info += f"\n\t-\tModel cost priority {i}, found {c}, waited {cost[i]} "
    if not mr.cost:
        info = "NO COST ; TEST IGNORED"
    
    return ret,info
            


def func_trueinone(mr,arg):
    if not isinstance(arg, set):
        atoms = set(arg)

    ret = False5
    models = mr.models
    for m,i in zip(models,range(len(models))):
        m = set(m)
        if atoms.issubset(m):
            ret = True

    return ret,None


def func_exactsetall(mr, arg):
    if not isinstance(arg, set):
        atoms = set(arg)

    ret = True
    info = ""
    models = mr.models

    for m,i in zip(models,range(len(models))):
        m = set(m)
        if not atoms.issubset(m) or not m.issubset(atoms):
            ret = False
            info += f'\n    -\tMissing (-)/Not desired (+) symbol(s) on model {i} : \n\t\t'
            for s in atoms:
                if not s in m:
                    info +=  '(-) '+s + ' '
            
            for s in m:
                if not s in atoms:
                    info +=  '(+) '+s + ' '
                
    return ret,info



def func_exactsetone(mr, arg):
    if not isinstance(arg, set):
        atoms = set(arg)

    ret = False
    info = ""
    models = mr.models

    for m,i in zip(models,range(len(models))):
        m = set(m)
        if  atoms.issubset(m) and m.issubset(atoms):
            ret = True
    return ret,None


listTC = {
    'sat' : TestCaller('sat', func_sat),
    'trueinall': TestCaller('trueinall', func_trueinall),
    'modelcost': TestCaller('modelcost', func_modelcost),
    'trueinone' : TestCaller('trueinone', func_trueinone),
    'exactsetall' : TestCaller('exactsetall', func_exactsetall),
    'exacrsetone' : TestCaller('exactsetone', func_exactsetone)
}




