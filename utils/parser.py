
import re
from .model_register import *
import clingo.ast
# import textx









def parse(output):
    output = output.splitlines()
    models = []
    n_models = None
    isSAT = False
    modelCost = None

    for l,index in zip(output,range(len(output))):
        if re.match(r'Answer: [0-9]+', l) != None:

            models.append(output[index+1])
        if re.match(r'Models', l) != None:
            n_models = int(l.split(' ')[-1])
        if re.match(r'SATISFIABLE', l) != None:
            sat=True
        if re.match(r'OPTIMUM FOUND', l) != None:
            sat=True
        if re.match(r'Optimization', l) != None:
            modelCost= int(l.split(' ')[-1])
    

    if n_models != len(models):
        raise('[TO DEV] Error in the parsing')

    if models:
        for m,i in zip(models,range(len(models))) :
            models[i] = m.split(' ')
            
    if modelCost:
        models = [models[-1]]

    return {
        "models" : models,
        "isSat" : isSAT,
        "rawInput" : output,
        "modelCost" : modelCost
    }



def find_symbol(st,sym):
    ret = []
    for c,i in zip(st,range(len(st))):
        if c == sym:
            ret.append(i)
    if not ret:
        return [-1]
    return ret

def split_coma(st):
    parenthesis_count = 0
    landmark = 0
    ret = []
    fp = True
    for c,i in zip(st,range(len(st))):
        if c == '(' : 
            parenthesis_count +=1
            if fp :
                landmark = i
                fp = False
        if c == ')' : 
            parenthesis_count -=1
            if parenthesis_count == 0:
                ret.append(st[landmark+1:i])
        if c == ',' and parenthesis_count <= 1:
            ret.append(st[landmark+1:i])
            landmark = i
    
    return ret



def check_end_symbol(splited):
    ret = []
    for e in splited:
        if '(' not in e:
            ret.append(eval(e))
        else:
            ret.append(split_function(e))
    
    return ret



def split_function(f):
    # print(f)
    f_p = find_symbol(f, '(')[0]

    if f_p == -1:
        return {
            "symbol" : f,
            "parameters" : []
        }

    if f_p == 0:
        splited = split_coma(f)
        return splited



    name = f[:f_p]
    splited = split_coma(f)
    ret = {
        "symbol" : name,
        "parameters" : check_end_symbol(splited)
    }
    

    return ret

    

def parse_models(mdls):
    
    ret = []
    for sm in mdls:
        pm = []
        for f in sm:
            pm.append(split_function(f))

        ret.append(pm)

    return ret

def parse_prg(p):
    lines= p.splitlines()
    for l in lines:
        print(l)
        clingo.ast.parse_string(l,lambda m : print(m))  


            

            
# def parse_models(models):
#     ret = []
#     for m in models :





"""
hello(1,bonjour(3))
=> function : hello
    - parameters : [
        int : 1,
        function : bonjour
            - parameters : [
                int 3
            ]
    ]
"""








#!/usr/bin/env python

# import argparse
# import utils
# import sys
# import json
# import os
# import clingo


# # ctl = clingo.Control()
# # ctl.load('example/simpleTest.lp')
# # ctl.ground([("base", [])])
# # print(ctl.solve(on_model=print))
# # print('hello')

# # parser = argparse.ArgumentParser()
# # parser.add_argument('--file', type=str, required=False)
# # parser.add_argument('--folder', type=str, required=False)
# # args = parser.parse_args()


# # if args.folder and args.file:
# #     raise "A most one betweem --specificFile and --specificFile should be specified"

# # if args.file :
# #     if os.path.isfile(args.file):
# #         file = args.file
# #     else:
# #         raise f"File {args.file} not found" 
# # else :
# #     file = False


# # if args.folder :
# #     if os.path.isfolder(args.folder):
# #         folder = args.folder
# #     else:
# #         raise f"Folder {args.folder} not found" 
# # else :
# #     folder = '.'


# # print(folder)
# # print(file)

# # if file :
    







# if not sys.stdin.isatty(): 
#     output = sys.stdin.read()
#     p_output = utils.parse(output)
#     parsed_models = utils.parse_models(p_output['models'])
#     print(json.dumps(parsed_models, indent=2))

    
#     # utils.parse_prg(p_output['models'])
# else :
#     print('No input')