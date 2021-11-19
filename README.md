# Unit testing with clingo  :-1: :+1:

## Inspirations

- **Shift planning project**: Uses pytest [here](https://github.com/PotasscoSolutions/shiftplanning-awfm/blob/main/tests/unit_test.py)
- **Euf propagator**: Uses pytest [here](https://github.com/krr-up/euf_theory/blob/master/tests/test.py)
- **Ansunit**: A declarative approach [here](https://github.com/rndmcnlly/ansunit)
- **Product configuration**: Uses a self-made run file [here](https://github.com/krr-up/product-configuration/blob/tobias/language/tests/run.py)



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
- What is your workflow for building a program to the test of this one ? What kind of rep architecture are you using ? 
- Are you doing Unit test for your programs ? (other way of testing)
  - Do you have a customs Unit Test program ? How it is working ? Do you have ideas on how to improve it so far ?
- With which solver are you running your programs ? (Clingo, Clingodl, Tellingo...)
  - Are the results from your programs very differents than clingo results ?
- Do you use the python api to run your encodings or are you using the command line ? (bash?)
- Would you rather have your test written direclty in your code or on a separed file ?
- Would you rather code the Unit test by using a python framework or in a yaml/json/other format ?
- Might your uUnit test require interval check and/or regex check ?
- Does your code has often multiple solutions ? Or checking 1 solutions is usually enough
  - Only one model should sometimes satisfy the Unit test to pass or all of the models should pass the Unit Test ?
- Are you using Clorm ? Pyhton helper function for it ? 
- Are your encodings sometimes never end or time out (for specific instances ?) 
  - How do you handle these cases ?
  - how long do you usually wait ?
- Testing the cost of a model ?
- Are you using another encoding to see if your current encoding gives the right answer ? Comparing the number of stable models ?
- Should unit testing output be at a certain format or that dosn't matter ? (if command line with json, YAML...)

