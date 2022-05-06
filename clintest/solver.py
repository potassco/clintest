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
        ctl = self.prepare_ctl()      
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                model = Model(m)
                for e in self.evaluators:
                    if not e.done() : 
                        e.on_model(model)
           
            sr = handle.get()
            for e in self.evaluators:
                e.on_finish(sr)

        for r in self.retrieve_result():
            print(r)
        
    def prepare_ctl(self):
        try:
            ctl = self.ctls[self.function](self.argument)
        except:
            raise "Control object not recognized"

        for p in self.encoding:
            ctl.load(self.folder + p)
        ctl.ground([("base", [])])
        return ctl

    def retrieve_result(self):
        results = []
        for ev in self.evaluators:
            result = ev.conclude()
            result.add_solver(self)
            results.append(result)
        return results


    def __str__(self):
        ret = f"{self.function}, arguments : '{str(self.argument)}', encodings : {str(self.encoding)}\n"
        return ret
        

            


    
