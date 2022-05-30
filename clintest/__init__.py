from .solver import *
from .evaluator import *
from .test import *
import os
import sys
import inspect

class Clintest:
    def __init__(self,evaluatorfile:str=None,verbosity:int=0, outputfile:str=None):
        self.tests:List[Test] = []
        self.settings = {
            'evaluatorfile' : evaluatorfile,
            'verbosity' : verbosity,
            'outputfile' : outputfile
        }


        if self.settings['evaluatorfile']:
            if isinstance(self.settings['evaluatorfile'],str):
                self.load_evaluators(self.settings['evaluatorfile'])


    def load_evaluators(self,path:str):
        if '/' in path:
            path = os.path.abspath(path)
            module = path[path.rindex('/')+1:]
            path = path[:path.rindex('/')]
            sys.path.append(path)
        else : 
            module = path   

        for name, obj in inspect.getmembers(__import__(module)):
            if inspect.isclass(obj):
                if issubclass(obj,Evaluator):
                    Evaluator.evaluator_dict[name] = obj
    
    def add(self, test):
        self.tests.append(test)

    def load(self, path:str):
        if isinstance(path,list):
            if len(path) == 0 :
                path.append('*.json')
            for p in path:
                pl = verify_path(p)
                if len(pl) == 0 :
                    print('No test json file found.')
                    exit(0)
                self.load(pl[0])


        else :
            if os.path.isdir(path):
                path = verify_path(path)
            with open(path) as file:
                rawtests = JSON.load(file)
                for rawtest in rawtests:
                    self.add(Test.from_json(rawtest,folder=getFolder(path)))

    def run(self):
        for test in self.tests:
            test.run()

    def show_result(self):
        ret = ''
        for test in self.tests:
            ret = test.get_result(self.settings['verbosity'])

        if self.settings['outputfile']:
            with open(self.settings['outputfile'], 'w') as f:
                f.write(ret)
        else :
            print(ret)
