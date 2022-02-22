# Clintest 
*Helper program for unit test in ASP.*
## How to use
Clintest can be used in different ways :
- **Python script**
- **Command line** in progress
- **Piped from a command line Clingo call** in progress

### Writing a test Description
In order to perform test, Clintest require a description of the test that will be performed. The description of the unit-tests are made in json.
```json
// Example of test descriptions
{
    "encodingsFileList": [
        [
            "pathfinding.lp",
            "instances/instance01.lp",
            "optimization.lp"
        ]
    ],
    "controlParameters": [
        [
            "0"
        ]
    ],
    "testDescription": [
        {
            "testName": "Must be SAT - test instance01.lp",
            "functionName": "sat",
            "arguments": true
        },
        {
            "testName": "Must have reach the end",
            "functionName": "trueinall",
            "arguments": [
                "endreached"
            ]
        },
        {
            "testName": "Model cost test : 4",
            "functionName": "modelcost",
            "arguments": 4
        }
    ]
}
```

The json test object is devided by 3 sections.

|Key | Description| Parameters|
|-------|---------|---|
|**encodingsFileList** |Describe the encodings that Clintest must run before executing the test.| List of list of encodings files*|
|**controlParameters** |Describe the parameters to give to the clingo control object.| List of list of Control object parameters*| 
|**testDescription** |Describe the set of unit-test that will be executed.| List of unit test|
---
\* An euclidian multiplication of theses lists of lists will be executed in order to perform parameterized test. If you give 3 lists of encodings files and 3 lists of control parameters, 27 in total will be performed.

### Unit test
Unit test description required 3 parameters :
|Key | Description | Parameters|
|---|---|---|
|testName| Name of the test, only usefull for human reading|String|
|functionName|Function that will be executed on the models|Key string|
|arguments|Arguments that will be gived to the function|Depending of the function (see function table)|

### Test functions
A predefined set of test functions can be called with a unique identifier (string).

|Key string|Argument|Description|
|----------|---------|-----------|
|sat       |true\|false| Argument : true => test succeed if encoding result is satifiable <br>Argument : false => test succed if encoding result is unsatisfiable|
|trueinall|List of atoms|The list of atoms given have to be a subset of **every** output model|
|trueinone|List of atoms|The list of atoms given have to be a subset of **at lest one** output model|
|modelcost |Number| The last model should have a cost equal to the parameter given, ignored if no optimization|
|exactsetall|List of atoms|The list of atoms have to be equal to  **every** output model|
|exactsetone|List of atoms|The list of atoms have to be equal to  **at least one** output model|


Custom functions can be created and used in tests.

## Usage : Python script
### Quick example
Clintest is able to call (by default) Clingo before running test if no model register is given to the solving call of the tests.
Usage :

```python
# Example usage (clintest repo root directory)
>>> import clintest
>>> ct = clintest.Clintest(['example/pathfinding/satisfiability.json', 'example/pathfinding/test_instance01.json'])
>>> ct()
```
Output (might be different from actual version, however at least same datas are still available):
```console
Test #1.1  : Must be SAT
Configuration : {'controlParameters': ['0'], 'encodingsFileList': ['pathfinding.lp', 'instances/instance01.lp', 'optimization.lp']}
        Result PASS
Test #1.2  : Must be SAT
Configuration : {'controlParameters': ['0'], 'encodingsFileList': ['pathfinding.lp', 'instances/instance02.lp', 'optimization.lp']}
        Result PASS
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Test #1.1  : Must be SAT - test instance01.lp
Configuration : {'controlParameters': ['10'], 'encodingsFileList': ['pathfinding.lp', 'instances/instance01.lp']}
        Result PASS
Test #1.2  : Must be SAT - test instance01.lp
Configuration : {'controlParameters': ['10'], 'encodingsFileList': ['pathfinding.lp', 'instances/instance01.lp', 'optimization.lp']}
        Result PASS

Test #2.1  : Must have reach the end
Configuration : {'controlParameters': ['10'], 'encodingsFileList': ['pathfinding.lp', 'instances/instance01.lp']}
        Result PASS
Test #2.2  : Must have reach the end
Configuration : {'controlParameters': ['10'], 'encodingsFileList': ['pathfinding.lp', 'instances/instance01.lp', 'optimization.lp']}
        Result PASS

Test #3.1  : Model cost test : 4
Configuration : {'controlParameters': ['10'], 'encodingsFileList': ['pathfinding.lp', 'instances/instance01.lp']}
        Result PASS
        Additionnal informations : IGNORED
Test #3.2  : Model cost test : 4
Configuration : {'controlParameters': ['10'], 'encodingsFileList': ['pathfinding.lp', 'instances/instance01.lp', 'optimization.lp']}
        Result PASS
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Test executed in 0.00030422210693359375 ms
Result on call : Success
- - - - - - - - - - - -
```

**More "use case" on how to use it [here](https://github.com/krr-up/clintest/tree/clintest-ctl-approach/example/pathfinding]) or [here](https://github.com/krr-up/clintest/tree/clintest-ctl-approach/example/constexample)**

### Clintest Object - Python script
The Clintest contructor require as parameters a test source (test description path or a dictionnary object that is similar to the JSON object).
The object created by the constructor can be called with an optionnal Model Register (MR) that contains models. If a MR is given, keys **encodingFileList** and **controlParameters** will be ignore, no additionnal solving call will be called.



### Plug Clintest to my script ?
CLintest can be use in a "standalone" way, but also can be plug to custom script. In order to successfully plug clintest to your own custom script, additionnals step are required. given the following example :
```python
...
ctl = clingo.Control('0')
ctl.load('example/simpleexample/color.lp')
ctl.solve(on_model=print)
...
```
To simply add unit test to this little script you will need add thse lines :

```python
...
ctl = clingo.Control('0')
ctl.load('example/simpleexample/color.lp')
mr = clintest.ModelRegister()
ctl.solve(on_model=mr)
ct = clintest.Clintest(testobj)
ct(mr=mr)
...
```

With thes lines added, when the line 6 will be executed, the tests described by the 'testobj' (path or dictionnary object) will be executed and give similar result to previous examples.

### Custom functions
In progress, but if needed, modify file 'testcaller.py' to add custom testing functions. 
