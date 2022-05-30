import clingo

from typing import Any, List, Sequence
from .evaluator import EvaluatorContainer
from .model import *




class Solver:
    ctls = {
        "clingo": clingo.Control
    }

    def __init__(self, function: str, argument: List[str], encoding: List[List[str]], instance: List[str], folder: str = ""):
        self.function = function
        if not isinstance(argument,List) : argument = [argument]

        self.argument = argument
        
        self.encoding = encoding + instance
        self.folder = folder

    def from_json(json:dict):
        if not 'instance' in json:
            instance = []
        else:
            instance = json['instance']
        solver = Solver(function=json['function'],
                        argument=json['argument'],
                        encoding=json['encoding'],
                        instance=instance,
                        folder=json['folder'])
        return solver

    def prepare_ctl(self):
        try:
            ctl = self.ctls[self.function](self.argument)
        except:
            raise "Control object not recognized"

        for p in self.encoding:
            ctl.load(self.folder + p)
        ctl.ground([("base", [])])
        return ctl

    def run(self, ec:EvaluatorContainer) -> EvaluatorContainer:
        ctl = self.prepare_ctl()
        with ctl.solve(yield_=True) as hnd:
            for m in hnd:
                ec.on_model(m)
            ec.on_finish(hnd.get())
        return ec

    def __str__(self):
        ret = f"{self.function}, arguments : '{str(self.argument)}', encodings : {str(self.encoding)}\n"
        return ret