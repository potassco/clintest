from .__init__ import *
import json as JSON
import sys
import argparse
import glob


def init_argparse():
    parser = argparse.ArgumentParser(description='Path of test descriptions')
    parser.add_argument('paths', metavar='path', type=str, nargs='*', help='string (path) list', default=glob.glob('**/*.json'))
    args   = parser.parse_args()
    return args



if __name__ == '__main__':
    if not sys.stdin.isatty(): 
        # # Init parser
        # args = init_argparse()

        # # Getting informations
        # rawinput    = sys.stdin.read()
        # jsoninput   = JSON.loads(rawinput)


        # if len(args.paths) > 1 :
        #     print('WARNING : calling piped Clintest with multiple testfiles might not behave as you intended  (ignoring configuration)')

        # ## Loading testfile
        # paths = args.paths
        # evaluators = []
        # for p in paths:
        #     with open(p) as file:
        #         j = JSON.loads(file)
        #         je = j['evaluator']
        #         evaluators.append(evaluator_dict[je["function"]].from_json(je))
        
        
        raise Exception("Not implemmented yet")

    else :
        args = init_argparse()
        w = Worker()
        w.load(args.paths)
        w.run()