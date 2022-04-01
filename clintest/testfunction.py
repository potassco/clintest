class TestFunction:
    def __init__(self,on_type='on_model',call=None):
        self.call = call
        self.on_type = on_type

    def __call__(self, result, argument):
        return self.call(result,argument)
        

def is_satisfiable(result,argument):
    if (result.satisfiable and argument) or (not result.satisfiable and not argument) :
        return True
    else :

        return False




ct_issat = TestFunction(on_type='on_finish',call=is_satisfiable)