# import clintest as ct
# import clingo


# def func_trueinone(mr,arg):
#     if not isinstance(arg, set):
#         atoms = set(arg)

#     ret = False
#     info = ""
#     models = mr.models

#     for m,i in zip(models,range(len(models))):
#         m = set(m)
#         if  atoms.issubset(m):
#             ret = True
                
#     return ret,info
    

# custom_function = ct.TestCaller('trueinone', func_trueinone)
# globalTC = ct.collectTestCallers([custom_function])





# test = [{
#         "testName": "True in one 'rain'",
#         "functionName": "trueinone",
#         "arguments": ['rain']
#     }]

# mr = ct.ModelRegister()



# ctl = clingo.Control('0')
# ctl.load('example.lp')
# ctl.ground([("base", [])])

# ctl.solve(on_model=mr)
# # print(ct.runTestFromTestDesc(test, mr, ct.jsonTC))
# print(ct.runTestFromTestDesc(test, mr, globalTC))



# def euclidianConfiguration(array, init=[],index=0):
#         if index >= len(array):
#             return init
#         else :
#             if init :
#                 n_init = []
#                 for a in init:
#                     for b in array[index]:
#                         mem = a.copy()
#                         for key in b:
#                             if key in a:
#                                 raise Exception('Error key')
#                             else:
#                                 mem[key] = b[key]
#                         n_init.append(mem)
#                 return euclidianConfiguration(array,init=n_init, index=index+1) 
#             else :
#                 n_init = array[0]
#                 return euclidianConfiguration(array,init=n_init, index=index+1) 
    
    

# test = [

# ]

# print(euclidianConfiguration(test))

import clintest
# ct = clintest.Clintest(['example/pathfinding/satisfiability.json', 'example/pathfinding/test_instance01.json','example/pathfinding/test_instance02.json'])
ct = clintest.Clintest(['example/constexample/test_encoding.json'])

ct()