from .modelregister import *
import clintest.testcaller as testcaller

import clingo
import os
from os import listdir
from os.path import isfile, join
import json
import inspect

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class ClintestApp:
    def __init__(self):
        pass

    def run(self, folder):
        # retrieve functions in functions file
        test_functions = {}
        for f in vars(testcaller).values():
            if (str(type(f))) == "<class 'function'>":
                test_functions[f.__name__] = f

        # Retrieve all data in folder
        #TODO : try if the path exist
        path = folder
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
                                print(f'### TEST CASE {i+1} \t: {test["name"]}'.format())
                                ctl = clingo.Control("0")
                                mr = ModelRegister()
                                for file in test['file']:
                                    fullfile = path + file
                                    ctl.load(fullfile)

                                ctl.ground([("base", [])])
                                ctl.solve(on_model=mr,on_unsat=mr)

                                for test_case in test :
                                    if test_case != 'name' and test_case != 'file':
                                        try :
                                            arg =test[test_case]
                                            result, info = test_functions[test_case](mr,arg)
                                            if result : result = f'{style.GREEN}PASS{style.RESET}'
                                            else : result = f'{style.RED}FAIL{style.RESET}'
                                            print(f'##  RESULT : \t{result}')
                                            if info :
                                                print('Additional informations : ' + info)

                                                
                                        except KeyError:
                                            print('Function not available, pass test')
                                    

                            
                                                        
                            else :
                                print(f'Wrong format for test {i}')
                        



            except ValueError:
                pass
