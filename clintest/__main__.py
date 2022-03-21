from .clintest import *
from .parser import *
import json
import sys
import argparse

if __name__ == '__main__':
    if not sys.stdin.isatty(): 

        # Init parser
        parser = argparse.ArgumentParser(description='Path of test descriptions')
        parser.add_argument('paths', metavar='path', type=str, nargs='+', help='string (path) list', default='**/*.json')
        args   = parser.parse_args()

        # Getting informations
        rawinput    = sys.stdin.read()
        jsoninput   = json.loads(rawinput)
        model       = jsoninput['Call'][-1]['Witnesses'][-1]['Value']

        if 'Costs' in jsoninput['Call'][-1]['Witnesses'][-1]:
            cost        = jsoninput['Call'][-1]['Witnesses'][-1]['Costs']
        else :
            cost = None

        # Model register
        mr          = ModelRegister()
        mr.models   = model
        mr.cost     = cost
        if len(args.paths) > 1 :
            print('WARNING : calling piped Clintest with multiple testfiles might not behave as you intended  (ignoring configuration)')
        ct = Clintest(args.paths)
        ct(mr=mr)

    else :
        parser =argparse.ArgumentParser(description='Path of test descriptions\nExample : python -m clintest example/pathfinding/*.json')
        parser.add_argument('paths', metavar='path', type=str, nargs='+', help='string (path) list', default='**/*.json')
        args = parser.parse_args()
        ct = Clintest(args.paths)
        ct()

        