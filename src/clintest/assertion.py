"""The abstract class [`Assertion`][clintest.assertion.Assertion] and classes extending it."""

from abc import ABC, abstractmethod
from typing import Set, Union, override

from clingo.symbol import Symbol, parse_term

from .protocol import Model


def _into_symbol(symbol: Union[Symbol, str]) -> Symbol:
    if isinstance(symbol, Symbol):
        return symbol
    return parse_term(symbol)


class Assertion(ABC):
    """An assertion is a statement that may or may not hold for a certain model.

    Assertions operate on any object implementing the [`Model`][clintest.protocol.Model] protocol, including `clingo.solving.Model` and [`PersistedModel`][clintest.protocol.PersistedModel] instances.
    An assertion is necessary to assemble the [`Assert`][clintest.test.Assert] test.
    """

    @abstractmethod
    def holds_for(self, model: Model) -> bool:
        """Return whether this assertion holds for `model`.

        Args:
            model: The model to evaluate the assertion against.

        Returns:
            Whether this assertion holds for `model`.
        """


class Contains(Assertion):
    """An assertion that holds if a model contains a given `symbol`.

    This checks atom membership, independently of which symbols are shown.
    """

    def __init__(self, symbol: Union[Symbol, str]) -> None:
        """Initialize the assertion with `symbol`.

        Args:
            symbol: The symbol to check for.
                Strings are parsed using `clingo.symbol.parse_term`.
        """
        self.__symbol = _into_symbol(symbol)

    def __repr__(self):
        name = self.__class__.__name__
        return f'{name}("{self.__symbol}")'

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return model.contains(self.__symbol)


class Equals(Assertion):
    """An assertion that holds if a model's shown symbols equal the given set of `symbols`."""

    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        """Initialize the assertion with `symbols`.

        Args:
            symbols: The symbols that must exactly match the model's shown symbols.
                Strings are parsed using `clingo.symbol.parse_term`.
        """
        self.__symbols = {_into_symbol(s) for s in symbols}

    def __repr__(self):
        name = self.__class__.__name__
        symbols = {str(symbol) for symbol in self.__symbols}
        return f"{name}({symbols})"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return self.__symbols == set(model.symbols(shown=True))


class SubsetOf(Assertion):
    """An assertion that holds if a model's shown symbols are a subset of the given set of `symbols`."""

    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        """Initialize the assertion with `symbols`.

        Args:
            symbols: The symbols allowed among the model's shown symbols.
                Strings are parsed using `clingo.symbol.parse_term`.
        """
        self.__symbols = {_into_symbol(s) for s in symbols}

    def __repr__(self):
        name = self.__class__.__name__
        symbols = {str(symbol) for symbol in self.__symbols}
        return f"{name}({symbols})"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return set(model.symbols(shown=True)).issubset(self.__symbols)


class SupersetOf(Assertion):
    """An assertion that holds if a model's shown symbols are a superset of the given set of `symbols`."""

    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        """Initialize the assertion with `symbols`.

        Args:
            symbols: The symbols required among the model's shown symbols.
                Strings are parsed using `clingo.symbol.parse_term`.
        """
        self.__symbols = {_into_symbol(s) for s in symbols}

    def __repr__(self):
        name = self.__class__.__name__
        symbols = {str(symbol) for symbol in self.__symbols}
        return f"{name}({symbols})"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return set(model.symbols(shown=True)).issuperset(self.__symbols)


class Optimal(Assertion):
    """An assertion that holds if the optimality of a model is proven."""

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return model.optimality_proven


class True_(Assertion):
    """The assertion that is true for each model."""

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return True


class False_(Assertion):
    """The assertion that is false for each model."""

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return False


class Not(Assertion):
    """The negation of a given assertion.

    This assertion holds if `operand` does not hold and vice versa.
    """

    def __init__(self, operand: Assertion) -> None:
        """Initialize the negation with `operand`.

        Args:
            operand: The assertion to negate.
        """
        self.__operand = operand

    def __repr__(self):
        name = self.__class__.__name__
        operand = repr(self.__operand)
        return f"{name}({operand})"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return not self.__operand.holds_for(model)


class And(Assertion):
    """The conjunction of a list of given assertions.

    This assertion holds if all `args` hold.
    """

    def __init__(self, *args: Assertion) -> None:
        """Initialize the conjunction with `args`.

        Args:
            *args: The assertions to combine.
        """
        self.__operands = args

    def __repr__(self):
        name = self.__class__.__name__
        operands = ", ".join(repr(operand) for operand in self.__operands)
        return f"{name}({operands})"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return all((operand.holds_for(model) for operand in self.__operands))


class Or(Assertion):
    """The disjunction of a list of given assertions.

    This assertion holds if any `args` hold.
    """

    def __init__(self, *args: Assertion) -> None:
        """Initialize the disjunction with `args`.

        Args:
            *args: The assertions to combine.
        """
        self.__operands = args

    def __repr__(self):
        name = self.__class__.__name__
        operands = ", ".join(repr(operand) for operand in self.__operands)
        return f"{name}({operands})"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return any((operand.holds_for(model) for operand in self.__operands))


class Implies(Assertion):
    """The implication of two given assertions.

    This assertion holds if `antecedent` holds implies that `consequent` holds.
    In other words, this assertion holds if `antecedent` does not hold or `consequent` holds.
    """

    def __init__(self, antecedent: Assertion, consequent: Assertion) -> None:
        """Initialize the implication with `antecedent` and `consequent`.

        Args:
            antecedent: The condition of the implication.
            consequent: The assertion required when the condition holds.
        """
        self.__antecedent = antecedent
        self.__consequent = consequent

    def __repr__(self):
        name = self.__class__.__name__
        antecedent = repr(self.__antecedent)
        consequent = repr(self.__consequent)
        return f"{name}({antecedent}, {consequent})"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        return not self.__antecedent.holds_for(model) or self.__consequent.holds_for(model)


class Equivalent(Assertion):
    """The equivalence of a list of given assertions.

    This assertion holds if all `args` simultaneously hold or not hold.
    """

    def __init__(self, *args: Assertion) -> None:
        """Initialize the equivalence with `args`.

        Args:
            *args: The assertions to combine.
        """
        self.__operands = args

    def __repr__(self):
        name = self.__class__.__name__
        operands = ", ".join(repr(operand) for operand in self.__operands)
        return f"{name}({operands})"

    @override
    def holds_for(self, model: Model) -> bool:  # noqa: D102
        operands = iter(self.__operands)

        try:
            first = next(operands).holds_for(model)
        except StopIteration:
            return True

        return all((first == operand.holds_for(model) for operand in operands))
