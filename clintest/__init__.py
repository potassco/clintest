## IMPORTS ##
from .modelregister import *
from .testcaller import *

import time
import clingo
import json

'''
    CLass style, helper class for better console output
'''
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

'''
    Function that verify that every eleement of an array are the same ase given
'''
def verifyElements(array,typeCheck):
    for e,i in zip(array,range(len(array))):
        if type(e) != typeCheck:
            return False
    return True


'''
    Function that change an array [[a1,a2],[b1,b2]] in a set of configuration 
        [[a1,b1],[a1,b2],[a2,b1],[a2,b2]]
    Used for parameterised tests
'''
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
    '''
        Class clintest
        @description clintest object, manage unit test (by default) for clingo
        @param source : source of anytype (path or disctionnary object) taht refer to a test flow description
        @param ctlConstroctor : (optionnal) Default : solver control object
    '''

    def __init__(self, source, ctlConstructor=clingo.Control):
        self.tests = []
        self.testResult = None
        conf = {
            "source" : source,
            "type"   : type(source)
        }
        self.source  = conf
        self.ctlConstructor = ctlConstructor
        self.collectTest(source)
        self.tcl = listTC


    def collectTest(self,source):
        '''
            function collectTest
            @description From the source that have been passed to the constructor, 
            load and preprocess the tests as a property of the CLintest Object
            @param source : the source to retrive and treat the test from

            source can be :
                - a list of path
                - a path (work in progress)
                - a list of dictionnary object
                - a dictionnary object
        '''
        if type(source) == type({}):
            source['folder']   = None
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
                if verifyElements(source, type({})):
                    for t in source:
                        t['folder']   = None
                        t['filename'] = None   
                    self.tests.append(t)

                # CASE : Is an array of path 
                elif verifyElements(source, type('')):
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
        '''
        function createConfiguration
        @description This function will create the set of different configuration that will be created and used
        for the test process (@use euclidianConfiguration).
        The different set of configuration are generated from the values identified by the keys controlParameters and encodingFileList
        @param t : test description object
        '''
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
            # print(t['encodingsFileList'])
            if verifyElements(t['encodingsFileList'], type([])):
                confElement = []
                for ctlarg in t['encodingsFileList']:
                    confElement.append({'encodingsFileList' : ctlarg})
                confs.append(confElement)
            elif verifyElements(t['encodingsFileList'], type('')):
                confs.append([{'encodingsFileList' : t['encodingsFileList']}])

        confs = euclidianConfiguration(confs)
        # print(confs)
        return confs
        

    def runTest(self,test,conf,mr):
        '''
        function runTest
        @description This function will run a test that have been given to the ModelRegister object.
        @param test : the test to run on the ModelRegister object mr
        @param conf : the configuration that have been used to create the ModelRegister object
        @param mr : ModelRegister object that contain the different model that tests will be proceed on
        '''
        if not mr:
            mr = ModelRegister()
            ctl = self.ctlConstructor(conf['controlParameters'])
            if test['folder']:
                for f in conf['encodingsFileList']:
                    ctl.load(test['folder']+f)
            else :
                for f in conf['encodingsFileList']:
                    ctl.load(f)
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
        '''
        function prettyPrint
        @description This function takes the output of the test workflow and create a pretty output to show to the user. 
        '''
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


    def __call__(self,mr=None,display=True):
        '''
        function __call__
        @description when called, this function will run the testworkflow
        @param mr : (optionnal) Default:None. ModelRegister object that the test description will be ran onto.
        @param display : (optionnal) Default:True. Call prettyPrint function at the en if True.

        @behavior if no ModeLRegister given, tests will then be run after solving the encodings discribed by the test object,
        that HAVE TO contain the property encodingFileList. Otherwise, all of the test will be run on the ModelRegister object,
        properties encodingFileList and controlConfiguration will then be ignored.
        '''
        for test in self.tests:
            confs = self.createConfiguration(test)
            for c in confs:
                self.runTest(test,c,mr)
        if display:
            self.prettyPrint()










