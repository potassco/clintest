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
    BOLD ='\033[1m'
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

    def __init__(self, source):
        self.tests = []
        self.testResult = []
        conf = {
            "source" : source,
            "type"   : type(source)
        }
        self.source  = conf
        self.ctlConstructor = {
            'clingo' : clingo.Control
        }
        self.collectTest(source)
        self.tcl = listTC


        self.confignore = None


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
                        if type(data) == type([]):
                            for test in data :
                                if '/' in file:    
                                    # print(file[:5])
                                    folder = file[:file.rindex('/')+1]  # Added for pretty print
                                    test['folder'] = folder
                                else :
                                    test['folder'] = './'
                                test['filename'] = file    # Added for pretty print
                                self.tests.append(test)
                        else :
                            if '/' in file:
                                folder = file[:file.rindex('/')+1]  # Added for pretty print
                                data['folder'] = folder
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

        default = {
            'function' : 'clingo',
            'argument' : ['0']
        }
        
        def fetchconf(key, t, default, flatten=True, required=True):
            if key in t:
                if type(t[key]) == type(""):
                    return [{key : t[key] }]
                elif verifyElements(t[key], type('')) and flatten:
                    confElement = []
                    for arg in t[key]:
                        confElement.append({key : arg})
                    return confElement
                elif verifyElements(t[key], type('')) and not flatten:
                    return [{key : t[key]}]
                elif verifyElements(t[key], type([])) and  flatten:
                    raise "Must be a list of string or string"
                elif verifyElements(t[key], type([])) and not flatten:
                    
                    confElement = []
                    for arg in t[key]:
                        confElement.append({key : arg})
                    return confElement

            else :
                if key in default :
                    return [{key : default[key]}]
                else :
                    if required:
                        raise f'{key} missing in default parameter, make sure value is available in run part of your test.'
                    else :
                        return [{key : []}]

        

        confs.append(fetchconf('function', t, default, required=True))
        confs.append(fetchconf('argument', t, default, required=True))
        confs.append(fetchconf('encoding', t, default, flatten=False,required=True))
        confs.append(fetchconf('instance', t, default, flatten=False, required=False))
        
        # function more configuration

        # Cleaning configuration
        clean_conf = []
        for c in confs:
            if c:
                clean_conf.append(c)

        confs = euclidianConfiguration(clean_conf)
        return confs
        


    def buildMR(self,conf,test):
        '''
        function buidMR
        @description run control onbject accoring to the parameters passed to create a ModelRegister object
        @param conf : configuration that will be used to configure/run the controller
        @param test : test containing informations such as folder etc
        '''
        ## Function here "controler" configuration and extention.
        mr = ModelRegister()
        ctl = self.ctlConstructor[conf['function']](conf['argument'])
        if test['folder']:
            for f in (conf['instance'] + conf['encoding']):
                ctl.load(test['folder']+f)

        ctl.ground([("base", [])])
        ctl.solve(on_model=mr,on_unsat=mr)

        return mr


    def runTest(self,test,mr,conf):
        '''
        function runTest
        @description This function will run a test that have been given to the ModelRegister object.
        @param test : the test to run on the ModelRegister object mr
        @param conf : the configuration that have been used to create the ModelRegister object
        @param mr : ModelRegister object that contain the different model that tests will be proceed on
        '''
        start = time.time()
        data = {}
        args = test['argument']
        fname = test['function']
        result, info = self.tcl[fname](mr, args)
        data['time'] = time.time() - start
        data['success'] = result
        data['info'] = info
        data['name'] = test['name']
        data['configuration'] = conf
        return data

            


    def prettyPrint(self):
        '''
        function prettyPrint
        @description This function takes the output of the test workflow and create a pretty output to show to the user. 
        '''
        finalSuccess = True
        totaltime = 0
        globalsuccess = True

        for test in self.testResult:
            print(f'\n{style.BOLD}{style.UNDERLINE}{test["name"].upper()}{style.RESET}\n')
            for unittest,i in zip(test['evaluate'],range(len(test['evaluate']))):
                for result,j in zip(unittest['result'],range(len(unittest['result']))):
                    totaltime += result['time']
                    if len(unittest['result'])>1:
                        print(f'Test #{i+1}.{j+1}  : {unittest["name"]}')
                    else:
                        print(f'Test #{i+1} on : {unittest["name"]}')
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
        if finalSuccess:
            print(f'{style.BOLD}Result on call : {style.GREEN}Success{style.RESET}')
        else:
            print(f'{style.BOLD}Result on call :  {style.RED}Fail{style.RESET}')
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')



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
            test = test.copy()
            ## Function here "preprocessing"
            confs = self.createConfiguration(test['run'])
            
            if mr:
                for evaluation,i in zip(test['evaluate'],range(len(test['evaluate']))):
                    if not 'result' in evaluation:
                        evaluation['result'] = []
                    evaluation['result'].append(self.runTest(evaluation,mr,self.confignore))
            else :
                if not confs:
                    raise "No configuration, check intergrity, keys of the run part"
                for c in confs:
                    mr = self.buildMR(c,test)
                    for evaluation,i in zip(test['evaluate'],range(len(test['evaluate']))):
                        if not 'result' in evaluation:
                            evaluation['result'] = []
                        evaluation['result'].append(self.runTest(evaluation,mr,c))
            self.testResult.append(test)

        if display:
            self.prettyPrint()










