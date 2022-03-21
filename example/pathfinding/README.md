# Path finding example
The encoding pathefinding.lp try to solve a pathfinding problem. The robot (square) try to reach his goal (circle) the fastest way possible if the file optimization is included in the clingo call.

## Satisfiability.json
This test file contain only satisfiability test, however, the key "**encodingFileList**" contains 2 set of files, this way, the satisfiability test will be executed 2 times.
This example contain two instances :
![Instance01](instances/instance01.png)
![Instance02](instances/instance02.png)

Here is the satisfiability file :
```json
{
    "name" : "Satisfiability of pathfinding",
    "run" :{
        "function" : ["Clingo"],
        "argument" : ["0"],
        "encoding" : ["pathfinding.lp", "optimization.lp"],
        "instance"  : [["instances/instance01.lp"],["instances/instance02.lp"]]
    },
    "evaluate" : [{
        "name"      : "Must be SAT",
        "function"  : "sat",
        "argument"     : true 
    }]
}
```
SATISFIABILITY OF PATHFINDING

Test #1.1  : Must be SAT
Configuration : {'function': 'Clingo', 'argument': '0', 'encoding': ['pathfinding.lp', 'optimization.lp'], 'instance': ['instances/instance01.lp']}
        Result PASS
Test #1.2  : Must be SAT
Configuration : {'function': 'Clingo', 'argument': '0', 'encoding': ['pathfinding.lp', 'optimization.lp'], 'instance': ['instances/instance02.lp']}
        Result PASS
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Test executed in 8.344650268554688e-06 ms
Result on call : Success
- - - - - - - - - - - -
```

## test_instance01.json
The file test_instance,json contain a more in depth test of the encoding.
```json
{
    "encodingsFileList": [
        [
            "pathfinding.lp",
            "instances/instance01.lp"
        ],
        [
            "pathfinding.lp",
            "instances/instance01.lp",
            "optimization.lp"
        ]
    ],
    "controlParameters": [
        [
            "10"
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
The 3 tests described by the value of the key **testDescription** will test :
1. Satisfiability
2. The atom endreached exist in all model computed
3. The cost of the model is equal to 4 (in **instance01**, when **optimization.lp** is called, robot needs at least 4 "moves" to reached his goal)

