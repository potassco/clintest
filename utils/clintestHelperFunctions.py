def isSat(m):
    if (m.isSat):
        return True
    else :
        return False

def trueInAll(m,atoms):
    print(m)
    
    if not isinstance(atoms, set):
        atoms = set(atoms)

    models = m['models']

    for m in models:
        m = set(m)
        if not atoms.issubset(m):
            return False

    return True

def trueInOne(m,atoms):
    
    if not isinstance(atoms, set):
        atoms = set(atoms)

    models = m['models']

    for m in models:
        m = set(m)
        if atoms.issubset(atoms):
            return True

    return False


def exactSet(m,atoms):
    if not isinstance(atoms, set):
        atoms = set(atoms)
    
    models = m['models']

    for m in models:
        m = set(m)
        if atoms != m:
            return False

    return True

def modelCost(m,nb):
    if m['modelCost'] == nb:
        return True
    else :
        return False

    




print(exactSet({'models':[[1]]}, [1,2]))