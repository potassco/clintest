# Clintest: *framework for unit test in ASP.* :+1: :-1:

A framework for (unit)testing ASP programs. Clintest can be used as a standalone framework or as an API that contains multiple tools in order to performs tests.
This version is a prototype ; bugs and errors might still exist, do not hesitate creating issues on the github page.


## Examples
Given the following ecncoding *color.lp* :
```ASP
node(1..6).
edge(
    (1,2); (1,3); (1,4);
    (2,4); (2,5); (2,6);
    (3,4); (3,5);
    (5,6)
).


color(red; green; blue).
{ assign(N, C) : color(C) } = 1 :- node(N).
:- edge((N, M)), assign(N, C), assign(M, C).

#show assign/2.
```

In order to perform a test, Clintest require a description of the test that will be performed. The description of tests are made in json.
```json
[{
    "name" : "Basic tests for color.lp",
    "solver": {
        "function": ["clingo"],
        "argument": ["0"],
        "encoding": ["color.lp"]
    },
    "evaluator": [{
        "name": "color.lp is satisfiable",
        "function": "SAT",
        "argument": true
    }]
}]

```
In the little example above, on call, Clintest will create an instance of Clingo controller that will run the encodings *color.lp* with clingo with argument "0" for the controller. And then will check on the result of the execution, if the result is satisfiable or not.


## Writing a test description

The json test object is devided by 3 sections.

|Key | Description|
|-------|---------|
|**name** | Name of the test section |
|**solver** | Describe the solver process |
|**evaluator** | Describe the set of unit-test described with the Evaluator class that will be executed.|

The **solver** and **evaluator** sections are sub-json object described in Solver and Evaluators section.

---


### Solver
Solver section required 3 (+1) parameters :
|Key | Description |
|---|---|
| function | Solver that will be used to solve the encoding(s)|
| argument | Argument(s) that will be passed to the solver controller|
| encoding | Encoding(s) that the solver controller will solve|
|(optional) instances | instance(s) that will added to solving process|


The argument, encoding and instance section can contain multiple values in order to perform the same test on different set of encodings, instances and arguments. For instance :
```json

"solver": {
        "function": ["clingo"],
        "argument": [["0 --const c=1"], ["0 --const c=2"]],
        "encoding": [["e1.lp"],["e2.lp"]],
        "instance": ["instance01.lp"]
}
```
With this configuration we will obtain 4 different call :
- clingo, arg(0 --const c=1), e1.lp, instance01.lp 
- clingo, arg(0 --const c=2), e1.lp, instance01.lp 
- clingo, arg(0 --const c=1), e2.lp, instance01.lp 
- clingo, arg(0 --const c=2), e2.lp, instance01.lp 



### Evaluators (or unit-test functions)
A predefined set of evaluator (test functions) can be called with a unique identifier (string).

|Key string|Argument|Description|
|----------|---------|-----------|
|SAT       |true\|false| Argument : true => test succeed if encoding result is satifiable <br>Argument : false => test succed if encoding result is unsatisfiable|
|TrueInAll|List of atoms|The list of atoms given have to be a subset of **every** output model|
|TrueInOne|List of atoms|The list of atoms given have to be a subset of **at lest one** output model|
|ModelCost (not implemented yet) |Number| The last model should have a cost equal to the parameter given, ignored if no optimization|



## Custom evaluator
In order tu create your custom evaluators, you have to create object extending Evaluator abstract class.
Evaluator class contain multiple function that can be overwritten :
 - conclude(self) -> EvaluatorResult : force the evaluator to return a result
 - done(self) -> Boolean : return true if the evaluator is done evaluating (UNKNOWN -> False | FAIL, IGNORED and PASS -> True)
 - **on_model**(self,result) -> None : process method of a Model object (called * time)
 - **on_finish**(self,result) -> None : process method of a SolveResult
 - **\_\_init__**(self,name,function,argument) : can be overwritten in order to have custom variables/behavior/other

Once custom evaluators are defined in a file, you can use the option **--evaluator-file**=file to load the custom evaluators or by using the  parameters c = Clinest(**evaluator_file**=path) when creating a Clintest object.

As instance:
```python
from clintest import Evaluator, EvaluatorResult, ResultType
class CustomEvaluator(Evaluator):
    def __init__(self, name:str, function:str, argument:Any):
        super().__init__(name, function, argument)
        self.custom_variable = "something"
        
    def on_model(self, result):
        #... Do some fun testing

    def conclude(self) -> EvaluatorResult:
        # fixing result, if needed
        return super().conclude()

```

On the on_model call, a Model object will be given as argument, this model object contain some predefined properties/method that are defined as defined for a clingo Model. 


By default, conclude method will directly return an EvaluatorResult based, result of the test and on the properties of the evaluator. However you can stil overwrite the method to ground the result the result of the evaluator (conclude is the last method that will be called in the process) ; having a result that is UNKNOWN will throw an error.


Other examples are available in the clintest/evaluator.py file.


## Usage : Clintest in command line
Clintest can be called in shell. Since packaging deployement is not implemented yet, usage can only be done from root directory of package

```commandline
python --help
python -m clintest path [path*]
```

## Usage : Python script
### Quick example
Clintest is able to call (by default) Clingo before running test if no model register is given to the solving call of the tests.
Usage :

```python
# Example usage (clintest repo root directory)
ct = Clintest()
ct.load('examples/color')
ct.run()
ct.show_result()
```

## Usage : Plug it to your own script
```python
from clintest import Clintest, Evaluator, EvaluatorContainer, ResultType, TrueInAll, TrueInOne 
import clingo 

class CustomSAT(Evaluator):
    def __init__(self, name, function, argument):
        super().__init__(name, function, argument)

    def on_finish(self, result):
        print("I'm a different SAT than Evaluator.SAT")
        if not(self.argument ^ result.satisfiable):
            self.result = ResultType.SUCCESS
        else:
            self.result = ResultType.FAIL


ec = EvaluatorContainer([
    CustomSAT("color.lp is satisfiable", 'SAT', True),
    TrueInAll("Testing true in all", "trueinall", ["assign(1,red)"]),
    TrueInOne("Testing true in one", "trueinone", ["assign(5,blue)"])
])


ctl = clingo.Control('0')
ctl.load('./examples/color/color.lp')
ctl.ground([("base", [])])
ctl.solve(on_finish=ec.on_finish, on_model=ec.on_model)


for result in ec.conclude():
    print(result)

```



