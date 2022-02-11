

class ModelRegister:
    def __init__(self):
        self.models = []
        self.solveResult = []
        self.cost= None

    def __call__(self,arg):
        if str(type(arg)) == "<class 'clingo.solving.Model'>":
            model = []
            self.cost = arg.cost
            for s in arg.symbols(shown=True):
                model.append(s.__str__())
            self.models.append(model)
            

