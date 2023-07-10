from abc import ABC, abstractmethod
from typing import Set, Union

from clingo.solving import Model
from clingo.symbol import Symbol, parse_term


def _into_symbol(symbol: Union[Symbol, str]) -> Symbol:
    if isinstance(symbol, Symbol):
        return symbol
    return parse_term(symbol)


class Assertion(ABC):
    @abstractmethod
    def holds_for(self, model: Model) -> bool:
        pass


class Contains(Assertion):
    def __init__(self, symbol: Union[Symbol, str]) -> None:
        self.__symbol = _into_symbol(symbol)

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}(\"{self.__symbol}\")"

    def holds_for(self, model: Model) -> bool:
        return model.contains(self.__symbol)


class Equals(Assertion):
    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        self.__symbols = {_into_symbol(s) for s in symbols}

    def __repr__(self):
        name = self.__class__.__name__
        symbols = {str(symbol) for symbol in self.__symbols}
        return f"{name}({symbols})"

    def holds_for(self, model: Model) -> bool:
        return self.__symbols == set(model.symbols(shown=True))


class SubsetOf(Assertion):
    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        self.__symbols = {_into_symbol(s) for s in symbols}

    def __repr__(self):
        name = self.__class__.__name__
        symbols = {str(symbol) for symbol in self.__symbols}
        return f"{name}({symbols})"

    def holds_for(self, model: Model) -> bool:
        return set(model.symbols(shown=True)).issubset(self.__symbols)


class SupersetOf(Assertion):
    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        self.__symbols = {_into_symbol(s) for s in symbols}

    def __repr__(self):
        name = self.__class__.__name__
        symbols = {str(symbol) for symbol in self.__symbols}
        return f"{name}({symbols})"

    def holds_for(self, model: Model) -> bool:
        return set(model.symbols(shown=True)).issuperset(self.__symbols)


class True_(Assertion):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def holds_for(self, model: Model) -> bool:
        return True


class False_(Assertion):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def holds_for(self, model: Model) -> bool:
        return False


class Not(Assertion):
    def __init__(self, operand: Assertion) -> None:
        self.__operand = operand

    def __repr__(self):
        name = self.__class__.__name__
        operand = repr(self.__operand)
        return f"{name}({operand})"

    def holds_for(self, model: Model) -> bool:
        return not self.__operand.holds_for(model)


class And(Assertion):
    def __init__(self, *args: Assertion) -> None:
        self.__operands = args

    def __repr__(self):
        name = self.__class__.__name__
        operands = ", ".join(repr(operand) for operand in self.__operands)
        return f"{name}({operands})"

    def holds_for(self, model: Model) -> bool:
        return all((operand.holds_for(model) for operand in self.__operands))


class Or(Assertion):
    def __init__(self, *args: Assertion) -> None:
        self.__operands = args

    def __repr__(self):
        name = self.__class__.__name__
        operands = ", ".join(repr(operand) for operand in self.__operands)
        return f"{name}({operands})"

    def holds_for(self, model: Model) -> bool:
        return any((operand.holds_for(model) for operand in self.__operands))
