import json as JSON
import clingo
from .utils import *
from .runner import *
from .evaluator import *



class Worker:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def load(self, path):
        with open(path) as file:
            rawtests = JSON.load(file)
            for rawtest in rawtests:
                self.add(Test.from_json(rawtest,folder=getFolder(path)))

    def run(self):
        for test in self.tests:
            test.run()



class Test:
    def __init__(self, name, folder='./'):
        self.name = name
        self.folder = folder
        self.runners = []
        self.evaluators = []

    def from_json(json,folder='./'):
        test = Test(json['name'],folder=folder)

        confs = createConfigurations(json['runner'])
        for c in confs:
            c['folder'] = folder
            test.runners.append(Runner.from_json(c))
        

        for e in json['evaluator']:
            test.add_evaluator(evaluator_dict[e["function"]].from_json(e))

        return test

    def add_runner(self, runner):
        self.runners.append(runner)

    def add_evaluator(self, evaluator):
        self.evaluators.append(evaluator)

    def run(self):
        for r in self.runners:
            r.run(self.evaluators)
