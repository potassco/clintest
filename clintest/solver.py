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
        wrp = EvaluatorWrapper(self.evaluators) 
        ctl.solve(on_model=wrp.on_model,on_finish=wrp.on_finish)

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


class EvaluatorWrapper:
    def __init__(self, evaluators):
        self.evaluators = evaluators

    def on_model(self,result):
        for e in self.evaluators:
            e.on_model(Model(result))

    def on_finish(self, result):
        for e in self.evaluators:
            e.on_finish(result)

    def retrieve_result(self):
        return [e.conclude() for e in self.evaluators]  

        

            


    
