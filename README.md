# Unit testing with clingo  :-1: :+1:

## Inspirations

- **Shift planning project**: Uses pytest [here](https://github.com/PotasscoSolutions/shiftplanning-awfm/blob/main/tests/unit_test.py)
- **Euf propagator**: Uses pytest [here](https://github.com/krr-up/euf_theory/blob/master/tests/test.py)
- **Ansunit**: A declarative approach [here](https://github.com/rndmcnlly/ansunit)
- **Product configuration**: Uses a self-made run file [here](https://github.com/krr-up/product-configuration/blob/tobias/language/tests/run.py)
- https://github.com/potassco/clingo/tree/master/examples/clingo



## Interresting papers
- **Testing in ASP: Revisited Language and Programming Environment** : [here](https://link.springer.com/chapter/10.1007/978-3-030-75775-5_24)
- **A System for Random Testing in ASP** : [here](https://link.springer.com/chapter/10.1007/978-3-319-61660-5_21)


## Discussion points

- Use a testing package line pytest or something self made
- Have a python tests file or some more declarative approach like with a yaml
  
## Functionalities

- The framework should allow to tests clingo Applications
- Perform different queries clingos' answer
  - Is it SAT or UNSAT
  - Is a symbol in all or some answer set
  - Are two answers equal regardless of the order
  - Is one answer set contained in another
  - Union and intersection of answer sets
- An optional custom executable (bash script) to run the application including any preprocessing



## Questionnaire
### General questions
- What is your workflow for building a program ? What kind of "folder architecture" are you using ? 
- Are you doing Unit test for your programs ? (other way of testing)
  - Do you have a customs Unit Test program ? How it is working ? Do you have ideas on how to improve it so far ?
- Do you use the python api to run your encodings or are you using the command line ? (bash script?)
- For Unit testing, do you imagine testing a pyhton clingo application or your encoding output (from command line)
- With which solver are you running your programs ? (Clingo, ClingoDL, Tellingo...)
- Would you rather code the Unit Test by using pythons helper functions or in a yaml/json/other format ?
  - For only testing encodings, would you prefer write your encodings with ASP code format or another "language" (JSON, YAML...) ?
- in order to test your encodings, Would you rather have your test written direclty in your code or on a separed file ? 

### Advanced questions

- Might your Unit Test require interval check and/or (regex check) ?
- Are your encodings sometimes never end or time out (for specific instances ?) 
  - How do you handle these cases ?
  - Is a time out could be a testing case ? (same for memory usage ?)
- Would be the testing of the cost of a model a Unit test case for you ? (advanced, basic)
- Are you using another encoding to see if your current encoding gives the right answer ? Comparing the number of stable models ? (beyond UT)
- Should unit testing output be at a certain format or that doesn't matter ? (if command line with json, YAML...) 



### Questionaire answer [here](https://www.notion.so/Report-questionnaire-9c548b335bea4013973356088ddc3686)

## Python helper functions

|Python function   | Meaning   |
|---|---|
| isSat()  | Check if the output is satisfiable or not   |
| trueInAll(atoms)  | Check if the (list of) atom is in all answer set   |
| trueInOne(atoms)  | Check if the (list of) atom is in at least one answer set  |
| exactSet(atoms) | Check if the sets of given atoms is equal to the set of outputs atoms |
| modelCost(nb) | Check if the cost of the model is equal to a number (weak constraint) |


## Approaches
### Using a custom clingo application
Extending clingo application to handle the unit test ; adding a program called "clintest" in a .lp file with some custom rules to make the test such as :
- clintest(trueInAll, symbols(parameters)).

**Pros**
- Based on clingo app, up to date
- Based on clingo app, probably easy to extend
- Test wrote in ASP
- Can be wrote in a different file or in the same file
- We can probably add things on the work flow more than unit test
- Callable as a clingo command
- Test atoms not in the final result because it is a different program
- probably can fit with other app (clingodl, tellingo etc)

**Cons**
- Less control on the test workflow (order ...)
- (for now) not importable as a helper functions (MUST BE AT SOME POINT)
- ASP might not be the best way for writing test
- I'm not using the power of ASP to do the test, just the format and the parser
- Test cannot occurs at the same moment


### Using a application that read a pipe of clingo output
Creating an application that read the output of clingo such as :
- clingo 0 examples.lp | ./clintest

**Pros**
- easy to use
- nice to implement any approach
- test are being done afterwhile
- fit with bash script
- is a meta-exemple (makes sense ?) 
- can save the output (>) and test them "later"
- test completly distinct to the program

**Cons**
- /!\ require a parser, might not be up to date at some point
- not independent (need a pipe output)
- /!\ bug friendly because of parser


