import json as JSON
from .utils import *
from .solver import *
from .evaluator import *

import os
class Worker:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def load(self, path):
        if os.path.isdir(path):
            path = verify_path(path)

        if isinstance(path,list):
            for p in path:
                pl = verify_path(p)
                self.load(pl[0])
        else :
            with open(path) as file:
                rawtests = JSON.load(file)
                for rawtest in rawtests:
                    self.add(Test.from_json(rawtest,folder=getFolder(path)))

    def run(self):
        for test in self.tests:
            test.run()

    def add_evaluator(self, evaluator, key):
        evaluator_dict[key] = evaluator

class Test:
    def __init__(self, name, folder='./'):
        self.name = name
        self.folder = folder
        self.solvers = []

    def from_json(json,folder='./'):
        test = Test(json['name'],folder=folder)
        confs = createConfigurations(json['solver'])
        for c in confs:
            c['folder'] = folder
            s = Solver.from_json(c)
            for e in json['evaluator']:
                s.evaluators.append(evaluator_dict[e["function"]].from_json(e))
            test.solvers.append(s)
        return test

    def add_solver(self, solver):
        self.solvers.append(solver)


    def run(self):
        for r in self.solvers:
            r.run()

