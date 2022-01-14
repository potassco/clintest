import clintest as ct
import clingo


def func_trueinone(mr,arg):
    if not isinstance(arg, set):
        atoms = set(arg)

    ret = False
    info = ""
    models = mr.models

    for m,i in zip(models,range(len(models))):
        m = set(m)
        if  atoms.issubset(m):
            ret = True
                
    return ret,info
    

custom_function = ct.TestCaller('trueinone', func_trueinone)
globalTC = ct.collectTestCallers([custom_function])







test = [{
        "testName": "True in one 'rain'",
        "functionName": "trueinone",
        "arguments": ['rain']
    }]

mr = ct.ModelRegister()
print(ct.runTestFromJson(test, mr, ct.jsonTC))


ctl = clingo.Control('0')
ctl.load('example.lp')
ctl.ground([("base", [])])


ctl.solve(on_model=mr)


# print(ct.runTestFromJson(test, mr, globalTC))
