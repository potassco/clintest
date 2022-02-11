from .utils import *
import json

if __name__ == '__main__':
    if not sys.stdin.isatty(): 
        print('Piped')
        rawinput = sys.stdin.read()
        print(rawinput)
        if len(sys.argv)>1:
            ret = runTestFromPipeInput(rawinput, files=sys.argv[1], recurcive=False)
        else:
            ret = runTestFromPipeInput(rawinput, files= sys.argv[1], recurcive=False)

        print(json.dumps(ret,indent=4))
        prettyPrint(ret)
    else :
        tm = TestManager()
        tm.loadTestFromFile(files=sys.argv[1:])
        tm.run()