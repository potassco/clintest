

class ModelRegister:
    def __init__(self):
        self.models = []
        self.solveResult = []

    def __call__(self,arg):
        if str(type(arg)) == "<class 'clingo.solving.Model'>":
            model = []
            for s in arg.symbols(shown=True):
                model.append(s.__str__())
            self.models.append(model)





# print(vars(functions).values())
# my_module_functions = [f for _, f in vars(functions).values() if inspect.isfunction(f)]






    # ctl = clingo.Control()
    # ctl.load('example_configuration/test.lp')
    # ctl.ground([("base", [])])
    # print(ctl.solve(on_model=print))



# main()

