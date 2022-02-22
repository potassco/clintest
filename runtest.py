import clintest
import clingo

print('TEST #1 : testing Clintest object')
print('Test #1.1')
try:
    ct = clintest.Clintest()
    ct()
    print('TEST FAIL <=====')
except Exception as e:
    print('TEST PASS')


print('Test #1.2')
try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/color.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Must be SAT",
            "functionName"  : "sat",
            "arguments"     : True 
        }]
    }
    ct = clintest.Clintest(testobj)
    ct(display=False)
    print('TEST PASS')
except Exception as e:
    print(e)
    print('TEST FAIL <=====')

print('Test #1.3')
try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/color.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Must be SAT",
            "functionName"  : "sat",
            "arguments"     : True 
        }]
    }
    ct = clintest.Clintest([testobj])
    ct(display=False)
    print('TEST PASS')
except Exception as e:
    print(e)
    raise e
    print('TEST FAIL <=====')


print('Test #1.4')
try:
    testobj = {
        "encodingsFileList" : "example/simpleexample/color.lp",
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Must be SAT",
            "functionName"  : "sat",
            "arguments"     : True 
        }]
    }
    ct = clintest.Clintest([testobj])
    ct(display=False)
    print('TEST PASS')
except Exception as e:
    print(e)

    print('TEST FAIL <=====')

print('TEST #2 : using clintest as helper')
print('TEST 2.1')

try :
    testobj = {
        "testDescription" : [{
            "testName"      : "Must be SAT",
            "functionName"  : "sat",
            "arguments"     : True 
        }]
    }

    ctl = clingo.Control('3')
    ctl.load('example/simpleexample/color.lp')
    mr = clintest.ModelRegister()
    ctl.solve(on_model=mr)
    ct = clintest.Clintest([testobj])
    ct(display=False,mr=mr)
    print('TEST PASS')
except Exception as e:
    raise e
    print('TEST FAIL <=====ED')


print('TEST #3 : testing functions')
print('TEST 3.1 : sat')

try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/color.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Test sat",
            "functionName"  : "sat",
            "arguments"     : True 
        }]
    }
    ct = clintest.Clintest([testobj])
    ct(display=False)
    print('TEST PASS')
except Exception as e:
    print(e)
    print('TEST FAIL <=====')

print('TEST 3.2 : true in all')
try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/color.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Test true in all => Pass",
            "functionName"  : "trueinall",
            "arguments"     : ['green'] 
        }]
    }
    ct = clintest.Clintest([testobj])
    ct(display=True)
    print('TEST PASS')
except Exception as e:
    print(e)
    print('TEST FAIL <=====')


print('TEST 3.2 : true in all')
try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/color.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Test true in all => FAIL",
            "functionName"  : "trueinall",
            "arguments"     : ['blue'] 
        }]
    }
    ct = clintest.Clintest([testobj])
    ct(display=True)
    print('TEST PASS')
except Exception as e:
    print(e)
    print('TEST FAIL <=====')



print('TEST 3.3 : true in one')
try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/color.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Test true in one => Pass",
            "functionName"  : "trueinone",
            "arguments"     : ['blue'] 
        }]
    }
    ct = clintest.Clintest([testobj])
    ct(display=True)
    print('TEST PASS')
except Exception as e:
    print(e)
    print('TEST FAIL <=====')

print('TEST 3.4 : true in one')
try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/color.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Test true in one => Fail",
            "functionName"  : "trueinone",
            "arguments"     : ['notacolor'] 
        }]
    }
    ct = clintest.Clintest([testobj])
    ct(display=True)
    print('TEST PASS')
except Exception as e:
    print(e)
    print('TEST FAIL <=====')

print('TEST 3.5 : Model cost')
try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/testcostmodel.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Test model cost : right value => Pass",
            "functionName"  : "modelcost",
            "arguments"     : [1,-20,1] 
        }]
    }
    ct = clintest.Clintest([testobj])   
    ct(display=True)
    print('TEST PASS')
except Exception as e:
    print(e)
    print('TEST FAIL <=====')

print('TEST 3.6 : Model cost')
try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/testcostmodel.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Test Model cost, different size => Fail",
            "functionName"  : "modelcost",
            "arguments"     : [1] 
        }]
    }
    ct = clintest.Clintest([testobj])   
    ct(display=True)
    print('TEST PASS')
except Exception as e:
    print(e)
    print('TEST FAIL <=====')

print('TEST 3.7 : Model cost')
try:
    testobj = {
        "encodingsFileList" : ["example/simpleexample/testcostmodel.lp"],
        "controlParameters" : ["0"],
        "testDescription" : [{
            "testName"      : "Test model cost : wrong value => Fail",
            "functionName"  : "modelcost",
            "arguments"     : [1,1,1] 
        }]
    }
    ct = clintest.Clintest([testobj])   
    ct(display=True)
    print('TEST PASS')
except Exception as e:
    print(e)
    print('TEST FAIL <=====')