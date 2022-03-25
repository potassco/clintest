from .testfunction import *
class Evaluator:
    def __init__(self,name,function,argument):
        self.name = name
        self.function = function
        self.argument = argument
        self.function_object = eval(f'{self.function}')

    def from_json(jsonevaluator):
        return Evaluator(jsonevaluator['name'], jsonevaluator['function'], jsonevaluator['argument'])

    def __call__(self,result):
        return self.call(result)

    def call(self,result):
        out = self.function_object(result,self.argument)
        return out