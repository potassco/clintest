---
icon: lucide/bug
---

# Debugging Tests

When a test fails, its error message tells you which parts have failed, but not why.
clintest provides two wrappers to help: [`Record`][clintest.test.Record] shows what happened during solving, and [`Context`][clintest.test.Context] replaces the detailed report with a message of your choice.

Both wrap around an existing test and behave exactly like it, so you can use them anywhere a test is expected.

## Recording a test

Let's return to the failing test from [Getting Started](getting_started.md#your-first-test) and wrap it in a `Record`:

```python
from clintest.test import Assert, And, Record
from clintest.quantifier import All, Any
from clintest.assertion import Contains
from clintest.solver import Clingo

solver = Clingo(["0"], "a. {b}.")
test = And(
    Assert(Any(), Contains("a")),
    Assert(All(), Contains("b")),
    Assert(Any(), Contains("c")),
)

record = Record(test)
solver.solve(record)
```

Make sure to wrap the test before solving it.
A test that has already been solved cannot be solved again, so there would be nothing left to record.

Printing `record` shows the wrapped test, followed by the recording:

```pycon
>>> print(record.recording)
0: [T?] __init__
1: [F!] on_model
    a
2: [F!] on_statistics
3: [F!] on_finish
```

Each entry is a call the test received from the solver, together with the test's outcome after the call.
For `on_model`, the entry also lists the symbols of the model.

Here, the first model was `{a}`.
It does not contain `b`, so the test became certainly false right away.
clintest then stopped the solver, which is why the model `{a, b}` never appears.

## Recording part of a test

You do not have to record the whole test.
`Record` can wrap any test, including a single operand of `And` or `Or`:

```python
record = Record(Assert(Any(), Contains("a")))
test = And(
    record,
    Assert(All(), Contains("a")),
)
solver.solve(test)
```

```pycon
>>> print(record.recording)
0: [F?] __init__
1: [T!] on_model
    a
```

The recorded operand only received the first model, although the solver found two.
Once an operand's outcome is certain, `And` and `Or` stop passing calls to it, because its outcome can no longer change.
If you want to see all calls anyway, pass `ignore_certain=False` to `And` or `Or`:

```python
record = Record(Assert(Any(), Contains("a")))
test = And(
    record,
    Assert(All(), Contains("a")),
    ignore_certain=False,
)
solver.solve(test)
```

```pycon
>>> print(record.recording)
0: [F?] __init__
1: [T!] on_model
    a
2: [T!] on_model
    b a
3: [T!] on_statistics
4: [T!] on_finish
```

## Readable error messages

The detailed report of a failing test is helpful for you, but often too much for the people running your tests.
[`Context`][clintest.test.Context] lets you replace it with your own message.

Using a new instance of the test from [Getting Started](getting_started.md#your-first-test), this looks as follows:

```python
from clintest.test import Context

test = And(
    Assert(Any(), Contains("a")),
    Assert(All(), Contains("b")),
    Assert(Any(), Contains("c")),
)

context = Context(
    test,
    str_=lambda test: f"[{test.outcome()}] a and c must each appear in some model, and b in all.",
)
solver.solve(context)
```

The function passed as `str_` receives the wrapped test and returns its string representation.
This also changes the message of `assert_()`:

```pycon
>>> context.assert_()
Traceback (most recent call last):
  ...
AssertionError: The following test has failed.
    [F!] a and c must each appear in some model, and b in all.
```

Likewise, you can pass `repr_` to change the result of `repr()`.
