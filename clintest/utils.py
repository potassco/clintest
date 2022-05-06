import glob
import os

def fetchconf(key, t, default, flatten=True, required=True):
    if key in t:
        if type(t[key]) == type(""):
            return [{key: t[key]}]
        elif verifyElements(t[key], type('')) and flatten:
            confElement = []
            for arg in t[key]:
                confElement.append({key: arg})
            return confElement
        elif verifyElements(t[key], type('')) and not flatten:
            return [{key: t[key]}]
        elif verifyElements(t[key], type([])) and flatten:
            raise "Must be a list of string or string"
        elif verifyElements(t[key], type([])) and not flatten:

            confElement = []
            for arg in t[key]:
                confElement.append({key: arg})
            return confElement

    else:
        if key in default:
            return [{key: default[key]}]
        else:
            if required:
                raise f'{key} missing in default parameter, make sure value is available in run part of your test.'
            else:
                return [{key: []}]


def verifyElements(array, typeCheck):
    for e, i in zip(array, range(len(array))):
        if type(e) != typeCheck:
            return False
    return True


def euclidianConfiguration(array, init=[], index=0):
    if index >= len(array):
        return init
    else:
        if init:
            n_init = []
            for a in init:
                for b in array[index]:
                    mem = a.copy()
                    for key in b:
                        if key in a:
                            raise Exception('Error key')
                        else:
                            mem[key] = b[key]

                    n_init.append(mem)
            return euclidianConfiguration(array, init=n_init, index=index+1)
        else:
            n_init = array[0]
            return euclidianConfiguration(array, init=n_init, index=index+1)


def createConfigurations(jsonsolver):
    confs = []

    default = {
        'function': 'clingo',
        'argument': ['0']
    }

    confs.append(fetchconf('function', jsonsolver, default, required=True))
    confs.append(fetchconf('argument', jsonsolver, default, required=True))
    confs.append(fetchconf('encoding', jsonsolver, default,
                 flatten=False, required=True))
    confs.append(fetchconf('instance', jsonsolver, default,
                 flatten=False, required=False))

    # function more configuration

    # Cleaning configuration
    clean_conf = []
    for c in confs:
        if c:
            clean_conf.append(c)

    confs = euclidianConfiguration(clean_conf)
    return confs



def getFolder(path):
    ret = path[:path.rindex('/')+1]
    return ret



def verify_path(path):
    if os.path.isdir(path):
        if path[-1] == '/' : path += '**.json'
        else : path += '/**.json'
    return glob.glob(path)