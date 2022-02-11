from .modelregister import *
# from .utils import *
from .testcaller import *
import time
import clingo
import json

# TODO:
#   - Adding vocabulary clearness : In progress (better)
#   - More configuration on the json file : In progress
#   - More options functions (application callable directly) : In Progress
#   - - - TODO next
#   - Do actual parameters things for command line



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


def verifyElements(array,typeCheck):
    for e,i in zip(array,range(len(array))):
        if type(e) != typeCheck:
            return False
    return True

def euclidianConfiguration(array, init=[],index=0):
        if index >= len(array):
            return init
        else :
            if init :
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
                return euclidianConfiguration(array,init=n_init, index=index+1) 
            else :
                n_init = array[0]
                return euclidianConfiguration(array,init=n_init, index=index+1) 
    

class Clintest:
    tests = []
    testResult = None

    def __init__(self, source, ctlConstructor=clingo.Control):
        conf = {
            "source" : source,
            "type"   : type(source)
        }
        self.source  = conf
        self.ctlConstructor = ctlConstructor
        self.collectTest(source)
        self.tcl = listTC

    def collectTest(self,source):
        if type(source) == type({}):
            source['folder']    = None
            source['filename'] = None
            self.tests.append(source)

        elif type(source) == type(""):
            if '.json' in source:
                    file = source
                    with open(file) as j:
                        data = json.load(j)
                    if '/' in file:    
                        data['folder'] = file[:file.rindex('/')+1]  # Added for pretty print
                    else :
                        data['folder'] = './'
                    data['filename'] = file    # Added for pretty print
                    self.tests.append(data)

        # CASE : Is an array
        elif type(source) == type([]):
            if source:
                # CASE : Is an array of dictionnary
                if type(source[0]) == type({}):
                    for t in source:
                        source['folder']   = None
                        source['filename'] = None   
                    self.tests += source

                # CASE : Is an array of path 
                elif type(source[0]) == type(""):
                    for file in source:
                        with open(file) as j:
                            data = json.load(j)
                        if '/' in file:    
                            data['folder'] = file[:file.rindex('/')+1]  # Added for pretty print
                        else :
                            data['folder'] = './'
                        data['filename'] = file    # Added for pretty print
                        self.tests.append(data)

                else :
                    raise Exception(f"Wrong array's elements :{type(source[0])}")
            else :
                raise Exception('Empty list given')
        else:
            raise Exception(f"Wrong input type : {type(source)}")

    def createConfiguration(self,t):
        confs = []

        if 'controlParameters' in t :
            if verifyElements(t['controlParameters'], type([])):
                confElement = []
                for ctlarg in t['controlParameters']:
                    confElement.append({'controlParameters' : ctlarg})
                confs.append(confElement)
            else :
                confs.append([{'controlParameters' : t['controlParameters']}])
        else:
            confs.append([{'controlParameters' : '0'}])


        if 'encodingsFileList' in t :
            if verifyElements(t['encodingsFileList'], type([])):
                confElement = []
                for ctlarg in t['encodingsFileList']:
                    confElement.append({'encodingsFileList' : ctlarg})
                confs.append(confElement)
            else :
                confs.append([{'encodingsFileList' : t['encodingsFileList']}])

        confs = euclidianConfiguration(confs)
        # print(confs)
        return confs
        

    def runTest(self,test,conf,mr):
        if not mr:
            mr = ModelRegister()
            ctl = self.ctlConstructor(conf['controlParameters'])
            for f in conf['encodingsFileList']:
                ctl.load(test['folder']+f)
            ctl.ground([("base", [])])
            ctl.solve(on_model=mr,on_unsat=mr)
        for t in test['testDescription']:
            start = time.time()
            data = {}
            args = t['arguments']
            fname = t['functionName']
            result, info = self.tcl[fname](mr, args)

            data['time'] = time.time() - start
            data['success'] = result
            data['info'] = info
            data['testName'] = t['testName']
            data['configuration'] = conf
            if 'result' in t :
                t['result'].append(data)
            else :
                t['result'] = [data]


    def prettyPrint(self):
        finalSuccess = True
        totaltime = 0
        globalsuccess = True

        for test in self.tests:
            for unittest,i in zip(test['testDescription'],range(len(test['testDescription']))):
                print()
                for result,j in zip(unittest['result'],range(len(unittest['result']))):
                    totaltime += result['time']
                    if len(unittest['result'])>1:
                        print(f'Test #{i+1}.{j+1}  : {unittest["testName"]}')
                    else:
                        print(f'Test #{i+1} on : {unittest["testName"]}')
                    print(f"Configuration : {result['configuration']}")
                    if result['success'] :
                        print(f"\tResult {style.GREEN}PASS{style.RESET}")
                    else:
                        print(f"\tResult {style.RED}FAIL{style.RESET}")
                    if result['info'] :
                        print(f'\tAdditionnal informations : {result["info"]}')

                    globalsuccess = globalsuccess and result['success']
            print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
            finalSuccess = finalSuccess and globalsuccess
        print(f'Test executed in {totaltime} ms' )
        if finalSuccess:
            print(f'Result on call : {style.GREEN}Success{style.RESET}')
        else:
            print(f'Result on call : {style.RED}Fail{style.RESET}')
        print('- - - - - - - - - - - -')


    def __call__(self,mr=None):
        for test in self.tests:
            confs = self.createConfiguration(test)
            for c in confs:
                self.runTest(test,c,mr)
        self.prettyPrint()









