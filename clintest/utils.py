from .testcaller import *
from .modelregister import *
from .parser import *
from os import listdir
from os.path import isfile, join, isdir
import clingo
import sys
import json
import time
import glob


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


class TestManager:
    testlist = []
    ctlConstructor = clingo.Control



    def __init__(self, testCallerModule=None):
        self.TCS = self.collectTestCallers()

    def collectTestCallers(self, moduleName=[]):
        # QUESTION : other smart ways of gettings all the functions
        if type(moduleName) != type([]):
            moduleName = [moduleName]
        tcs = {}
        for tc in (listTC + moduleName):
            tcs[tc.name] = tc

        return tcs


    def loadTestFromFile(self,files=[]):
        if files:
            for file in files:
                if '.json' in file:
                    with open(file) as j:
                        data = json.load(j)
                    if '/' in file:    
                            data['folder'] = file[:file.rindex('/')+1]  # Added for pretty print
                    else :
                        data['folder'] = './'
                    data['filename'] = file    # Added for pretty print
                    self.testlist.append(data)
        else:
            raise Exception('No files given')


    def runTestFromTestDesc(self, testdesc, mr, tcs):
        ret = []
        for test, n in zip(testdesc, range(len(testdesc))):
            start = time.time()
            data = {}
            args = test['arguments']
            fname = test['functionName']
            result, info = tcs[fname](mr, args)

            data['time'] = time.time() - start
            data['success'] = result
            data['info'] = info
            data['testName'] = test['testName']
            data['test'] = test
            ret.append(data)

        return ret

    
        

    def runTestFromTestFile(self, testfile,mr,tcs):
        if type(testfile) != type([]):
            testfile = [testfile]

        ret = []
        for tf in testfile :
            r = self.runTestFromTestDesc(tf['testDescription'], mr, tcs)
            for a in r:
                a['folder'] = tf ['folder']
                a['filename'] = tf ['filename']
                
            ret.append(r)

        return ret

    def run_solver(self,paths, ctlarg='0'):
        mr = ModelRegister()
        ctl = self.ctlConstructor(ctlarg)
        for p in paths:
            ctl.load(p)
        
        ctl.ground([("base", [])])
        ctl.solve(on_model=mr,on_unsat=mr)
        return mr
        




    def run(self):
        for f in self.testlist:
            print(f'File : {f["filename"]}')
            if 'controlParameters' in f:
                for arg in f['controlParameters']:
                    mr = self.run_solver([f['folder']+encoding for encoding in f['encodingsFileList']],ctlarg = arg)
                    output = self.runTestFromTestFile(f, mr, self.TCS)
                    # print(output)
                    output[-1][-1]['ctlarg'] = arg
                    self.prettyPrint(output)
            else :
                mr = self.run_solver([f['folder']+encoding for encoding in f['encodingsFileList']])
                output = self.runTestFromTestFile(f, mr, self.TCS)
                self.prettyPrint(output)

    

    def prettyPrint(self,output):
        finalSuccess = True
        # print(output)
        totaltime = 0
        for file in output:
            globalsuccess = True
            for test,i in zip(file,range(len(file))):
                totaltime += test['time']
                print(f'Test {i+1} on file : {test["filename"]}')
                print(f'Test name : {test["testName"]}')
                if 'ctlarg' in test :
                    print(f'ctl arguments : "{test["ctlarg"]}"')


                if test['success'] :
                    print(f"Result {style.GREEN}PASS{style.RESET}")
                else:
                    print(f"Result {style.RED}FAIL{style.RESET}")
                if test['info'] :
                    print(f'Additionnal informations : {test["info"]}')
                globalsuccess = globalsuccess and test['success']
            print('- - - - - - - - - - - - ')
            finalSuccess = finalSuccess and globalsuccess
        print(f'Test executed in {totaltime} ms' )
        if finalSuccess:
            print(f'Result on call : {style.GREEN}Success{style.RESET}')
        else:
            print(f'Result on call : {style.RED}Fail{style.RESET}')
        print('- - - - - - - - - - - - \n')






def retrieveTestFromFiles(files='**', recursive=True):
    if isdir(files) : 
        if files[-1] != '/' : files += '/**'
        else : files += '**'
    listfiles = glob.glob(files, recursive=recursive)
    ret = []
    print(files)
    for f in listfiles:
        try:
            if f.index('.json'):
                with open(f) as j:
                    data = json.load(j)
                if '/' in f:    
                    data['folder'] = f[:f.rindex('/')+1]  # Added for pretty print
                else :
                    data['folder'] = './'
                data['filename'] = f    # Added for pretty print
                ret.append(data)

        except ValueError:
            # print(f'{style.UNDERLINE}DEBUG:{style.RESET} File not considered : {f}')
            pass

    return ret






def runTestFromTestDesc(testdesc, mr, tcs):
    ret = []
    for test, n in zip(testdesc, range(len(testdesc))):
        start = time.time()
        data = {}
        args = test['arguments']
        fname = test['functionName']
        result, info = tcs[fname](mr, args)

        data['time'] = time.time() - start
        data['success'] = result
        data['info'] = info
        data['testName'] = test['testName']
        data['test'] = test
        ret.append(data)

    return ret



def run(files, additionnalCallers=[]):
    tcs = collectTestCallers(additionnalCallers)
    testdesclist = retrieveTestFromFiles(files=files,recursive=True)

    for testdesc in testdesclist:
        print(f'File : {testdesc["filename"]}')

         # Clingo call
        if 'controlParameters' in testdesc:
            ctl = clingo.Control(testdesc['controlParameters'])
        else :
            ctl = clingo.Control('0')

        mr = ModelRegister()
        for file in testdesc['encodingsFileList']:
            fullfile = testdesc["folder"] + file
            ctl.load(fullfile)

        ctl.ground([("base", [])])
        ctl.solve(on_model=mr, on_unsat=mr)

        output = runTestFromTestDesc(testdesc['testDescription'], mr, tcs)
        prettyPrint(output)



    
    



    

def runTestFromTestFile(testfile,mr,tcs):
    if type(testfile) != type([]):
        testfile = [testfile]

    ret = []
    for tf in testfile :
        r = runTestFromTestDesc(tf['testDescription'], mr, tcs)
        for a in r:
            a['folder'] = tf ['folder']
            a['filename'] = tf ['filename']
            
        ret.append(r)

    return ret

def runTestFromPipeInput(rawintput,files='**',recurcive=False, additionnalCallers=[]):
    tcs = collectTestCallers(additionnalCallers)
    mr= ModelRegister()
    pinput = parse(rawintput)
    mr.models = pinput['models']
    tcs = collectTestCallers(additionnalCallers)
    testfile = retrieveTestFromFiles(files=files,recursive=recurcive)
    ret= runTestFromTestFile(testfile, mr, tcs)
    return ret
