"""
The abstract class `clintest.assertion.Assertion` and classes extending it.
"""

from abc import ABC, abstractmethod
from typing import Set, Union

from clingo.solving import Model
from clingo.symbol import Symbol, parse_term


def _into_symbol(symbol: Union[Symbol, str]) -> Symbol:
    if isinstance(symbol, Symbol):
        return symbol
    return parse_term(symbol)


class Assertion(ABC):
    """
    An assertion is a statement that may or may not hold for a certain `clingo.model.Model`.
    As such, one is necessary to assemble the `clintest.test.Assert` test.
    """

    @abstractmethod
    def holds_for(self, model: Model) -> bool:
        """
        Returns whether this assertions holds for `model`.

        Parameters
        ----------
        model
            A `clingo.model.Model`.


        Returns
        -------
        Whether this assertions holds for `model`.
        """


class Contains(Assertion):
    """
    An assertion that holds if a model contains a given `symbol`.

    Parameters
    ----------
    symbol
        The `clingo.symbol.Symbol` or a `str` that can be parsed into a `clingo.symbol.Symbol` with `clingo.symbol.parse_term`.
    """

    def __init__(self, symbol: Union[Symbol, str]) -> None:
        self.__symbol = _into_symbol(symbol)

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}(\"{self.__symbol}\")"

    def holds_for(self, model: Model) -> bool:
        return model.contains(self.__symbol)


class Equals(Assertion):
    """
    An assertion that holds if the symbols of a model are equals to a given set of `symbols`.

    Parameters
    ----------
    symbols
        A set of `clingo.symbol.Symbol`s or `str`s that can be parsed into a `clingo.symbol.Symbol`s with `clingo.symbol.parse_term`.
    """

    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        self.__symbols = {_into_symbol(s) for s in symbols}

    def __repr__(self):
        name = self.__class__.__name__
        symbols = {str(symbol) for symbol in self.__symbols}
        return f"{name}({symbols})"

    def holds_for(self, model: Model) -> bool:
        return self.__symbols == set(model.symbols(shown=True))


class SubsetOf(Assertion):
    """
    An assertion that holds if the symbols of a model are a subset of a given set of `symbols`.

    Parameters
    ----------
    symbols
        A set of `clingo.symbol.Symbol`s or `str`s that can be parsed into a `clingo.symbol.Symbol`s with `clingo.symbol.parse_term`.
    """

    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        self.__symbols = {_into_symbol(s) for s in symbols}

    def __repr__(self):
        name = self.__class__.__name__
        symbols = {str(symbol) for symbol in self.__symbols}
        return f"{name}({symbols})"

    def holds_for(self, model: Model) -> bool:
        return set(model.symbols(shown=True)).issubset(self.__symbols)


class SupersetOf(Assertion):
    """
    An assertion that holds if the symbols of a model are a superset of a given set of `symbols`.

    Parameters
    ----------
    symbols
        A set of `clingo.symbol.Symbol`s or `str`s that can be parsed into a `clingo.symbol.Symbol`s with `clingo.symbol.parse_term`.
    """

    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        self.__symbols = {_into_symbol(s) for s in symbols}

    def __repr__(self):
        name = self.__class__.__name__
        symbols = {str(symbol) for symbol in self.__symbols}
        return f"{name}({symbols})"

    def holds_for(self, model: Model) -> bool:
        return set(model.symbols(shown=True)).issuperset(self.__symbols)


class True_(Assertion):
    """
    The assertion that is true for each model.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def holds_for(self, model: Model) -> bool:
        return True


class False_(Assertion):
    """
    The assertion that is false for each model.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def holds_for(self, model: Model) -> bool:
        return False


class Not(Assertion):
    """
    The negation of a given assertion.
    This assertion holds if `operand` does not hold and vice versa.

    Parameters
    ----------
    operand
        The `Assertion` to be negated.
    """

    def __init__(self, operand: Assertion) -> None:
        self.__operand = operand

    def __repr__(self):
        name = self.__class__.__name__
        operand = repr(self.__operand)
        return f"{name}({operand})"

    def holds_for(self, model: Model) -> bool:
        return not self.__operand.holds_for(model)


class And(Assertion):
    """
    The conjunction of a list of given assertions.
    This assertion holds if all `args` hold.

    Parameters
    ----------
    args
        The `Assertion`s to be combined.
    """

    def __init__(self, *args: Assertion) -> None:
        self.__operands = args

    def __repr__(self):
        name = self.__class__.__name__
        operands = ", ".join(repr(operand) for operand in self.__operands)
        return f"{name}({operands})"

    def holds_for(self, model: Model) -> bool:
        return all((operand.holds_for(model) for operand in self.__operands))


class Or(Assertion):
    """
    The disjunction of a list of given assertions.
    This assertions hold if any `args` hold.

    Parameters
    ----------
    args
        The `Assertion`s to be combined.
    """

    def __init__(self, *args: Assertion) -> None:
        self.__operands = args

    def __repr__(self):
        name = self.__class__.__name__
        operands = ", ".join(repr(operand) for operand in self.__operands)
        return f"{name}({operands})"

    def holds_for(self, model: Model) -> bool:
        return any((operand.holds_for(model) for operand in self.__operands))
