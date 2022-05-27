from .__init__ import *
import json as JSON
import sys
import argparse
import glob


def init_argparse():
    parser = argparse.ArgumentParser(description='Path of test descriptions')
    parser.add_argument('paths', metavar='path', type=str, nargs='*',
                        help='string (path) list', default=glob.glob('**/*.json'))
    parser.add_argument('--verbosity', metavar='verbosity', type=int,
                        help='Detail level for the output 0 -> All, 1 -> Reduced ...', default=0)
    parser.add_argument('--evaluator-file', metavar='evaluatorfile', type=str,
                        help='Path to custom evaluator (withou .py)', default=None)

    parser.add_argument('--output-file', metavar='outuputfilefile', type=str,
                        help='path to output file', default=None)             
                        
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    if not sys.stdin.isatty():
        # # Init parser
        # args = init_argparse()

        # # Getting informations
        # rawinput = sys.stdin.read()
        # jsoninput = JSON.loads(rawinput)
        # print(JSON.dumps(jsoninput, indent=4))
        # models = [ModelFromJSON(model['Value'],number) for (model, number) in zip(
        #     jsoninput['Call'][0]['Witnesses'], range(len(jsoninput['Call'][0]['Witnesses'])))]
        # # solve_result =

        # if len(args.paths) > 1:
        #     print('WARNING : calling piped Clintest with multiple testfiles might not behave as you intended  (ignoring configuration)')

        # evaluators = []
        # # Loading testfile
        # paths = args.paths
        # for p in paths:
        #     with open(p) as file:
        #         j = JSON.load(file)
        #         for test in j:
        #             evaluators = []
        #             evs = test['evaluator']
        #             for ev in evs:
        #                 evaluators.append(
        #                     evaluator_dict[ev["function"]].from_json(ev))

        # for model in models:
        #     for e in evaluators:
        #         e.on_model(model)

        # for e in evaluators:
        #     print(e.conclude())
        pass
        

    else:
        args = init_argparse()
        ct = Clintest(verbosity=args.verbosity,evaluatorfile=args.evaluator_file, outputfile=args.output_file)
        ct.load(args.paths)
        ct.run()
        ct.show_result()
