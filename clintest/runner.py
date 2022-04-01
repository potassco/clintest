import clingo

class Runner:
    ctls = {
        "clingo": clingo.Control
    }


    def __init__(self, function, argument, encoding, instance, folder =""):
        self.function = function
        self.argument = argument
        self.encoding = encoding + instance
        self.folder = folder

    def from_json(json):
        if 'instance' in json:
            instance = []
        else:
            instance = json['instance']
        runner = Runner(function=json['function'],
                        argument=json['argument'],
                        encoding=json['encoding'],
                        instance=instance,
                        folder = json['folder'])
        return runner

    def run(self, callbacks):

        on_model_cb = [c for c in callbacks if c.type=="on_model"]
        on_finish_cb = [c for c in callbacks if c.type=="on_finish"]
        try:
            ctl = self.ctls[self.function](self.argument)
        except:
            raise "Control object not recognized"

        for p in self.encoding:
            ctl.load(self.folder + p)

        ctl.ground([("base", [])])

        with ctl.solve(yield_=True) as handle:
            for m in handle: 
                for c in on_model_cb:
                    c(m)

            
            sr = handle.get()
            for c in on_finish_cb:
                print(c(sr))
            


    
