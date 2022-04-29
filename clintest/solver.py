import clingo
from .model import *







class Solver:
    ctls = {
        "clingo": clingo.Control
    }

    def __init__(self, function, argument, encoding, instance, folder =""):
        self.function = function
        self.argument = argument
        self.encoding = encoding + instance
        self.folder = folder
        self.persistant_model = []
        self.evaluators = []

    def from_json(json):
        if not 'instance' in json:
            instance = []
        else:
            instance = json['instance']
        solver = Solver(function=json['function'],
                        argument=json['argument'],
                        encoding=json['encoding'],
                        instance=instance,
                        folder = json['folder'])
        return solver


    def run(self):
        on_model_cb = [c for c in self.evaluators if c.on_model()]
        on_finish_cb = [c for c in self.evaluators if c.on_finish()]
        try:
            ctl = self.ctls[self.function](self.argument)
        except:
            raise "Control object not recognized"

        for p in self.encoding:
            ctl.load(self.folder + p)

        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                model = Model(m)
                # self.persistant_model.append(m)
                for c in on_model_cb:
                    if not c.done() : 
                        c(model)
           
            sr = handle.get()
            for c in on_finish_cb:
                c(sr)

        result = []
        print('CLINTEST RESULT\n')
        for rh in on_finish_cb + on_model_cb:
            result = rh.conclude()
            result.add_solver(self)
            print(result)

    def __str__(self):
        ret = f"{self.function}, arguments : '{str(self.argument)}', encodings : {str(self.encoding)}\n"
        return ret
        

            


    
