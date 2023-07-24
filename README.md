# clintest

`clintest` is a Python framework that enables you to write efficient unit tests for `clingo` programs quickly.
Devising and running multiple tests is a simple as:

```python
from clintest.test import Assert, And
from clintest.quantifier import All, Any
from clintest.assertion import Contains
from clintest.solver import Clingo

solver = Clingo("0", "a. {b}.")
test = And(
    Assert(Any(), Contains("a")),
    Assert(All(), Contains("b")),
    Assert(Any(), Contains("c")),
)

solver.solve(test)
test.assert_()
```

For details, please read [the documentation](https://potassco.org/clintest/).
