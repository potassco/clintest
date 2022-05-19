# Clintest 
*Helper program for unit test in ASP.*
## Description


## Writing a test Description
In order to perform test, Clintest require a description of the test that will be performed. The description of the unit-tests are made in json.
```json
// Example of test descriptions
[{
    "name" : "Basic tests for color.lp",
    "solver": {
        "function": ["clingo"],
        "argument": ["0"],
        "encoding": ["color.lp"]
    },
    "evaluator": [{
        "name": "color.lp is satisfiable",
        "function": "is_sat",
        "argument": true
    },{
        "name": "Testing true in all",
        "function": "trueinall",
        "argument": ["assign(1,red)"]
    },{
        "name": "Testing true in one",
        "function": "trueinone",
        "argument": ["assign(5,blue)"]
    }]
}]

```

The json test object is devided by 3 sections.

|Key | Description| Parameters|
|-------|---------|---|
|**name** | Name of the test section | String |
|**solver** | Describe the solver process | Json sub-object describing solving process| 
|**evaluator** | Describe the set of unit-test described with the Evaluator class that will be executed.| List of evaluator|
---


## Unit test
Unit test description required 3 parameters :
|Key | Description | Parameters|
|---|---|---|
|name| Name of the test, only usefull for human reading|String|
|function|Function that will be executed on the models|Key string|
|argument|Arguments that will be gived to the function|Depending of the function (see function table)|

## Evaluators (or unit-test functions)
A predefined set of evaluator (test functions) can be called with a unique identifier (string).

|Key string|Argument|Description|
|----------|---------|-----------|
|is_sat       |true\|false| Argument : true => test succeed if encoding result is satifiable <br>Argument : false => test succed if encoding result is unsatisfiable|
|trueinall|List of atoms|The list of atoms given have to be a subset of **every** output model|
|trueinone|List of atoms|The list of atoms given have to be a subset of **at lest one** output model|
|modelcost (not implemented yet) |Number| The last model should have a cost equal to the parameter given, ignored if no optimization|
|exactsetall (not implemented yet)|List of atoms|The list of atoms have to be equal to  **every** output model|
|exactsetone (not implemented yet)|List of atoms|The list of atoms have to be equal to  **at least one** output model|


### Custom evaluator
In order tu create your custom evaluators, you have to create object extending Evaluator abstract class.
Evaluator class contain multiple function that can be overwritten :
 - conclude(self) -> EvaluatorResult : force the evaluator to return a result
 - done(self) -> Boolean : return true if the evaluator is done evaluating (UNKNOWN -> False | FAIL, IGNORED and PASS -> True)
 - **on_model**(self,result) -> None : process method of a Model object (called * time)
 - **on_finish**(self,result) -> None : process method of a SolveResult
 - **\_\_init__**(self,name,function,argument) : can be overwritten in order to have custom variables/behavior/other

Once the custom evaluator is set, it can now be added using the worker function add_evaluator(Evaluator,key).

As instance:
```python
class CustomEvaluator(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)
        self.custom_variable = "something"
        
    def on_model(self, result):
        #... Do some fun testing

    def conclude(self) -> EvaluatorResult:
        # fixing result, if needed
        return super().conclude()

existing_worker.add_evaluator(CustomEvaluator, "EvaluatorName") # loaded json test object can now use the "EvaluatorName" key to call the evaluator

existing_worker.run() 
```

On the on_model call, a Model object will be given as argument, this model object contain some predefined properties/method that are defined as defined for a clingo Model. If needed the Clingo Model object can be accessed using result._model. However, since Clingo Model can not be stored and exist only in the actual scope, if you want to store them, you can use the persist() method that allows you tu use the symbols() function at any time (symbols function do not require any parameters, will only provides same output as clingo (#show)).

The conclude method return an EvaluatorResult that need to use the property of the evaluator that are :
- result -> ResultType (UNKNOWN, PASS, FAIL and IGNORED).
- evaluator ->  the evaluator itself
- missing (optional) -> a dictionnary that provid missing symbols for model (for output)
- overload (optional) -> a dictionnary that provid overload symbols for model (for output)
- additional (optional -> String that contain informations that will be displayed in the ouput

By default, conclude method will directly return an EvaluatorResult based on the properties of the evaluator. However you can stil overwrite the method to "fix" the result of the evaluator (conclude is the last method that will be called in the process) ; having a result that is UNKNOWN will throw an error.


Other examples are available in the clintest/evaluator.py file.


## Usage : Clintest in command line
Clintest can be called in shell. Since packaging deployement is not implemented yet, usage can only be done from root directory of package

```commandline
python -m clintest path [path*] 
```

## Usage : Python script
### Quick example
Clintest is able to call (by default) Clingo before running test if no model register is given to the solving call of the tests.
Usage :

```python
# Example usage (clintest repo root directory)
>>> import clintest
>>> w = clintest.Worker()
>>> w.load('examples/color/')
>>> w.run()
```
Output (might vary from version to version):
```console
CLINTEST RESULT

Testing color.lp is satisfiable
solver : clingo, arguments : '0', encodings : ['color.lp']
Function        : is_sat
Arguments       : True
Result          : PASS

Testing Testing true in all
solver : clingo, arguments : '0', encodings : ['color.lp']
Function        : trueinall
Arguments       : ['assign(1,red)']
Result          : FAIL
Missing (-) and overload (+) symbols
Model 3:
         - assign(1,red)

Testing Testing true in one
solver : clingo, arguments : '0', encodings : ['color.lp']
Function        : trueinone
Arguments       : ['assign(5,blue)']
Result          : PASS
```




