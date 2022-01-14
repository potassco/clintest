from .testcaller import *
from .modelregister import *
from os import listdir
from os.path import isfile, join
import clingo
import sys
import json

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

def retrieveTestJsonFile(folder, recursive=False):
    # TODO : test if folder is a path + string
    # TODO : reccurcive test gathering
    if folder[-1] != '/':
        folder += "/"

    tfp = [folder+f for f in listdir(folder) if isfile(join(folder, f))]
    ret = []
    for f in tfp:
        try:
            if f.index('.json'):
                with open(f) as j:
                    data = json.load(j)
                    data['folder'] = folder  # Added for pretty print
                    data['filename'] = f    # Added for pretty print
                    ret.append(data)

        except ValueError:
            print(
                f'{style.UNDERLINE}DEBUG:{style.RESET} File not considered : {f}')
            pass
    return ret


def collectTestCallers(additionnalCallers):
    # QUESTION : other smart ways of gettings all the functions
    tcs = {}
    for tc in (listTC + additionnalCallers):
        tcs[tc.name] = tc

    return tcs


def runTestFromJson(testdesc, mr, tcs):
    #TODO : Use a json output instead of a print
    ret = ''
    success = True
    for test, n in zip(testdesc, range(len(testdesc))):
        ret += f"\nTEST {n}\t\t: {test['testName']}\n"
        args = test['arguments']
        fname = test['functionName']
        result, info = tcs[fname](mr, args)
        if result:
            result = f'{style.GREEN}PASS{style.RESET}'
        else:
            result = f'{style.RED}FAIL{style.RESET}'
            success = False
        ret += f'RESULT \t\t: {result}\n'
        if info:
            ret += f'Additional informations : {info}\n'
        
        if n+1 != len(testdesc):
            ret += '-----------------'
    ret += '\n--------------------------------------------------------------'
    if success:
        ret += f'\nGLOBAL RESULT ON SECTION : {style.GREEN}PASS{style.RESET}'
    else:
        ret += f'\nGLOBAL RESULT ON SECTION : {style.RED}FAIL{style.RESET}'
    ret += '\n--------------------------------------------------------------'
    
    return ret



def run(folder, additionnalCallers=[]):
    tcs = collectTestCallers(additionnalCallers)
    testdesclist = retrieveTestJsonFile(folder)

    for testdesc in testdesclist:
        print(f'\nTest section : {testdesc["testSectionName"]}')
        print(f'File : {testdesc["filename"]}')

         # Clingo call
        ctl = clingo.Control("0")
        mr = ModelRegister()
        for file in testdesc['encodingsFileList']:
            fullfile = testdesc["folder"] + file
            ctl.load(fullfile)

        ctl.ground([("base", [])])
        ctl.solve(on_model=mr, on_unsat=mr)

        output = runTestFromJson(testdesc['testList'], mr, tcs)
        print(output)