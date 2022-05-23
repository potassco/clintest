from typing import Optional, Callable, List
from clingo import Control, SolveResult
from clintest.evaluator import Evaluator, Result, Error
from clintest.model import Model
from clintest.solver import Solver
from clintest.test import Test

class Clingo(Solver):
    def __init__(self, files:List[str]=None, program:str="", arguments:List[str]=None):
        self.files=[] if files is None else files
        self.program=program
        self.arguments= [] if arguments is None else arguments

    def run(self,
            on_model:Callable[[Model],None], 
            on_finish:Callable[[SolveResult],None]):
        ctl = Control(arguments=self.arguments)
        for f in self.files:
            ctl.load(f)
        ctl.add("base",[],self.program)
        ctl.ground([("base",[])])
        ctl.solve(on_model=on_model,on_finish=on_finish)

class MissingAtoms(Error):

    def __init__(self, model:Model, atom:str):
        super().__init__(f"The atom '{atom}' is missing in the model")
        # self.model = model.persist
        self.atom = atom
    

class InAll(Evaluator):

    def __init__(self, atom:str):
        super().__init__(f"Atom {atom} is in all models")
        self.atom = atom 
    
    def on_model(self, model:Model) -> Optional[Result]:
        symbols_str=[str(s) for s in model.symbols()]
        if self.atom not in symbols_str:
            return Result.FAILURE([MissingAtoms(model,self.atom)])
        return None
    
    def on_finish(self, result) -> Result:
        return Result.SUCCESS()

class InSome(Evaluator):

    def __init__(self, atom:str):
        super().__init__(f"Atom {atom} is in some model")
        self.atom = atom 
    
    def on_model(self, model:Model) -> Optional[Result]:
        symbols_str=[str(s) for s in model.symbols(shown=True)]
        if self.atom in symbols_str:
            return Result.SUCCESS()
        return None
    
    def on_finish(self, result) -> Result:
        return Result.FAILURE([MissingAtoms(None,self.atom)])


solver = Clingo([],"{a;b;c}.",["0"])
evaluators = [InAll("a"), InSome("b")]
t =Test(solver=solver, evaluators=evaluators,description="My main test")
t.run()
t.show_result(0)

