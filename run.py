#!/usr/bin/env python

import argparse
import utils
import sys
import json
import os
import clingo


# ctl = clingo.Control()
# ctl.load('example/simpleTest.lp')
# ctl.ground([("base", [])])
# print(ctl.solve(on_model=print))
# print('hello')

# parser = argparse.ArgumentParser()
# parser.add_argument('--file', type=str, required=False)
# parser.add_argument('--folder', type=str, required=False)
# args = parser.parse_args()


# if args.folder and args.file:
#     raise "A most one betweem --specificFile and --specificFile should be specified"

# if args.file :
#     if os.path.isfile(args.file):
#         file = args.file
#     else:
#         raise f"File {args.file} not found" 
# else :
#     file = False


# if args.folder :
#     if os.path.isfolder(args.folder):
#         folder = args.folder
#     else:
#         raise f"Folder {args.folder} not found" 
# else :
#     folder = '.'


# print(folder)
# print(file)

# if file :
    







if not sys.stdin.isatty(): 
    output = sys.stdin.read()
    p_output = utils.parse(output)
    parsed_models = utils.parse_models(p_output['models'])
    print(json.dumps(parsed_models, indent=2))

    
    # utils.parse_prg(p_output['models'])
else :
    print('No input')