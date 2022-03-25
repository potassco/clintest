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

    ctls = {
        "clingo": clingo.Control
    }

    def __init__(self, name, folder='./'):
        self.name = name
        self.folder = folder
        self.runners = []
        self.evaluators = []


    
        

    def from_json(json,folder='./'):
        test = Test(json['name'],folder=folder)

        confs = createConfigurations(json['runner'])
        for c in confs:
            test.runners.append(Runner.from_json(c))
        

        for e in json['evaluator']:
            test.add_evaluator(Evaluator.from_json(e))



        return test

    def add_runner(self, runner):
        self.runners.append(runner)

    def add_evaluator(self, evaluator):
        self.evaluators.append(evaluator)

    def on_model(self,model):
        for evaluator in self.evaluators:
            if evaluator.function_object.on_type == "on_model":
                out = evaluator(model)
    
    def on_finish(self,solve_result):
        for evaluator in self.evaluators:
            if evaluator.function_object.on_type == "on_finish":
                out = evaluator(solve_result)
                print(out)


    def run(self):
        for runner in self.runners :
            ctl = self.ctls[runner.function](runner.argument)
            for e in runner.encoding:
                ctl.load(self.folder + e)
            ctl.ground([("base", [])])
            ctl.solve(on_model=self.on_model,on_finish = self.on_finish)
