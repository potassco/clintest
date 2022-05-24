from queue import Empty
from typing import Dict, Optional, Callable, List, Union
import textwrap
from clingo import Control, SolveResult, Model, StatisticsMap
from clintest.check import Check, Result, Error
from clintest.solver import Solver
from clintest.test import Test
NoneType = type(None)

class Clingo(Solver):
    def __init__(self, files:List[str]=None, program:str="", arguments:List[str]=None):
        self.files=[] if files is None else files
        self.program=program
        self.arguments= [] if arguments is None else arguments

    def run(self,check:Check):
        ctl = Control(arguments=self.arguments)
        for f in self.files:
            ctl.load(f)
        ctl.add("base",[],self.program)
        ctl.ground([("base",[])])
        ctl.solve(on_model=check.on_model,
                on_finish=check.on_finish,
                on_statistics=check.on_statistics)

    def __str__(self):
        return f"""
        Clingo solver with:
            arguments: {self.arguments}
            files: {self.files}
            program: {self.program}
        """

class MissingAtoms(Error):

    def __init__(self, model:Model, atom:str):
        super().__init__(f"The atom '{atom}' is missing in the model")
        self.atom = atom

class InAll(Check):

    def __init__(self, atom:str):
        # Flag to check all models and add multiple errors
        super().__init__(f"Atom {atom} is in all models")
        self.atom = atom 

    def on_model(self, model:Model) -> bool:
        symbols_str=[str(s) for s in model.symbols()]
        if self.atom not in symbols_str:
            self.answer = Result.failure([MissingAtoms(model,self.atom)])
            return False
    
    def on_finish(self, result) -> Result:
        if not self.answer:
            self.answer =  Result.success()

    @property
    def result(self)->Union[Result, NoneType]:
        return self.answer

class InAny(Check):

    def __init__(self, atom:str):
        # Flag to check all models
        super().__init__(f"Atom {atom} is in some model")
        self.atom = atom 
        self.answer = None
    
    def on_model(self, model:Model) -> bool:
        symbols_str=[str(s) for s in model.symbols(shown=True)]
        if self.atom in symbols_str:
            self.answer = Result.success()
            return False
    
    def on_finish(self, result: SolveResult) -> NoneType:
        if not self.answer:
            self.answer = Result.failure([MissingAtoms(None,self.atom)])

    @property
    def result(self)->Union[Result, NoneType]:
        return self.answer



class All(Check):

    def __init__(self, checks:List[Check]):
        # Flag to check all checks
        super().__init__(f"All the following checks are successful")
        self.checks = checks
        self.ongoing_checks = checks
    
    def on_model(self, model:Model) -> bool:
        still_ongoing = []
        for c in self.ongoing_checks:
            done = c.on_model(model) is False
            if not done:
                still_ongoing.append(c)
        self.ongoing_checks = still_ongoing
        return still_ongoing
    
    def on_finish(self, result: SolveResult) -> NoneType:
        for c in self.checks:
            c.on_finish(result)
    
    def on_statistics(self,step_statistics: StatisticsMap,
                        accumulated_statistics: StatisticsMap) -> NoneType:
        for c in self.checks:
            c.on_statistics(step_statistics, accumulated_statistics)

    @property
    def result(self):
        success = all(c.result.is_success for c in self.checks)
        if success:
            return Result.success()
        return Result.failure([Error("Some check failed")])


    @property
    def additional_info(self) -> str:
        sub_results = "\n".join(str(c) for c in self.checks)
        return textwrap.indent(sub_results, '\t\t')


solver = Clingo([],"{a;b;c}.",["0"])
checks = [InAll("a"), InAny("b")]
t =Test(solver=solver, check=All(checks),description="My main test")
t.run()
print(t)