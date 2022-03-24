import json

class Tests:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def load(self, path):
        with open(path) as file:
            tests = json.load(file)
            for test in tests:
                self.add(Test.from_json(test))

class Test:
    def __init__(self, name):
        self.name = name
        self.runners = []
        self.evaluators = []

    def from_json(json):
        test = Test(json['name'])
        # TODO
        return test

    def add_runner(self, runner):
        self.runners.append(runner)

    def add_evaluator(self, evaluator):
        self.evaluators.append(evaluator)

    def run(self):
        pass
