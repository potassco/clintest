import clingo

class ModelRegister:
    def __init__(self):
        self.models = []
        self.solveResult = []

    def __call__(self,arg):
        if str(type(arg)) == "<class 'clingo.solving.Model'>":
            self.models.append(arg.symbols(shown=False))
        elif str(type(arg)) == "<class 'clingo.solving.SolveResult'>":
            self.solveResult.append(arg)
        
def isSat(models):
    pass


class MCB:

    def __init__(self):
        self._models = []
        self._core = None
        self.last = None

    def on_core(self, c):
        self._core = c

    def on_model(self, m):
        self.last = (m.type, sorted(m.symbols(shown=True)))
        self._models.append(self.last[1])

    @property
    def core(self):
        return sorted(self._core)

    @property
    def models(self):
        return sorted(self._models)