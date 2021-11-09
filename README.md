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