from .solver import *
from .evaluator import *
from .test import *


class Clintest:
    def __init__(self):
        self.tests:List[Test] = []

    def add(self, test):
        self.tests.append(test)

    def load(self, path):
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
        for test in self.tests:
            test.show_result()

    