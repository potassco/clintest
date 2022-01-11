import clingo
import os
from os import listdir
from os.path import isfile, join
import json
import functions
import inspect

# print(vars(functions).values())
# my_module_functions = [f for _, f in vars(functions).values() if inspect.isfunction(f)]



class ModelRegister:
    def __init__(self):
        self.models = []
        self.solveResult = []

    def __call__(self,arg):
        if str(type(arg)) == "<class 'clingo.solving.Model'>":
            self.models.append(arg.symbols(shown=True))
        elif str(type(arg)) == "<class 'clingo.solving.SolveResult'>":
            self.solveResult.append(arg)



def main():
    # retrieve functions
    test_functions = {}
    for f in vars(functions).values():
        if (str(type(f))) == "<class 'function'>":
            test_functions[f.__name__] = f

    # Retrieve all data in folder
    #TODO : try if the path exist
    path = 'example_configuration'
    if path[-1] != '/':
        path += "/"
    onlyfiles = [path+f for f in listdir(path) if isfile(join(path, f))]
    
    

    for f in onlyfiles:
        try :
            if f.index('.json'):
                with open(f) as j:
                    data = json.load(j)
                    print(f'File name : {f}')

                    for test,i in zip(data,range(len(data))) :
                        if 'name' in test and 'file' in test:
                            print(f'TEST CASE {i+1} : {test["name"]}')
                            ctl = clingo.Control()
                            mr = ModelRegister()
                            for file in test['file']:
                                fullfile = path + file
                                ctl.load(fullfile)

                            ctl.ground([("base", [])])
                            ctl.solve(on_model=mr,on_unsat=mr)

                            print(mr.models)
                            

                           
                                                    
                        else :
                            print(f'Wrong format for test {i}')
                    



        except ValueError:
            pass




    # ctl = clingo.Control()
    # ctl.load('example_configuration/test.lp')
    # ctl.ground([("base", [])])
    # print(ctl.solve(on_model=print))



main()

