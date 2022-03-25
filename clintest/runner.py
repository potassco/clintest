

class Runner:
    def __init__(self, function, argument, encoding, instance):
        self.function = function
        self.argument = argument
        self.encoding = encoding + instance

    def from_json(json):
        if 'instance' in json:
            instance = []
        else:
            instance = json['instance']
        runner = Runner(function=json['function'],
                        argument=json['argument'],
                        encoding=json['encoding'],
                        instance=instance)
        return runner

    
