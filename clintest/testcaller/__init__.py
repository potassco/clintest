def sat(mr,arg):
    if mr.models:
        return True, None
    else :
        return False, None

def trueinall(mr,arg):
    if not isinstance(arg, set):
        atoms = set(arg)

    ret = True
    info = ""
    models = mr.models

    for m,i in zip(models,range(len(models))):
        m = set(m)
        if not atoms.issubset(m):
            ret = False
            info += f'\nMissing symbol(s) on model {i} : '
            for s in arg:
                if not s in m:
                    info += s + ' '
                


    return ret,info
    