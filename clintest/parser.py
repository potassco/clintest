
import re
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
            isSAT=True
        if re.match(r'OPTIMUM FOUND', l) != None:
            sat=True
        if re.match(r'Optimization', l) != None:
            modelCost= int(l.split(' ')[-1]) # WARNING
    

    if n_models != len(models):
        raise('[TO DEV] Error in the parsing')

    if models:
        for m,i in zip(models,range(len(models))) :
            models[i] = m.split(' ')
            
    if modelCost:
        models = [models[-1]]

    return {
        "models" : models,
        "sat" : isSAT,
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


            