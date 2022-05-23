from typing import Optional, List
import textwrap
from .solver import Solver
from .evaluator import Evaluator, Result
from .model import Model
from .utils import *

class Test:
    def __init__(self, 
                solver: Solver, 
                evaluators: List[Evaluator],
                description: str = ""):
        self.solver = solver
        self.evaluators = evaluators
        self.results = [None] * len(evaluators)
        self.description= description

    def on_model(self, model: Model):
        for idx, e in enumerate(self.evaluators):
            if self.results[idx] is None:
                self.results[idx] = e.on_model(model)
        if all(self.results):
            return False
            

    def on_finish(self, *args) -> None:
        for idx, e in enumerate(self.evaluators):
            if self.results[idx] is None:
                self.results[idx] = e.on_finish(*args)

    def run(self) -> None:
        self.solver.run(self.on_model,
                        self.on_finish)


    def show_result(self, verbose_level:int) -> None:
        print(BLUE + f"TEST: {self.description}" + END_COLOR)
        for idx, r in enumerate(self.results):
            print(textwrap.indent(str(self.evaluators[idx]), '\t'))
            print(textwrap.indent(str(r), '\t\t'))
