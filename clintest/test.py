from typing import Optional

import textwrap

from .solver import Solver
from .check import Check
from .utils import *

NoneType = type(None)

class Test:
    def __init__(self, 
                solver: Solver, 
                check: Check,
                description: str = ""):
        self.solver = solver
        self.check = check
        self.description= description

    def run(self) -> NoneType:
        self.solver.run(self.check)

    def __str__(self) -> str:
        s = BLUE + "--"*20 + "\n"
        s += self.description + "\n"
        s += "--"*20 + "\n" + END_COLOR 
        s += "SOLVER: " + str(self.solver) + "\n"
        s += str(self.check)
        return s