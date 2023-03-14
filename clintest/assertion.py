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

    def holds_for(self, model: Model) -> bool:
        return model.contains(self.__symbol)


class Equals(Assertion):
    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        self.__symbols = {_into_symbol(s) for s in symbols}

    def holds_for(self, model: Model) -> bool:
        return self.__symbols == set(model.symbols(shown=True))


class SubsetOf(Assertion):
    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        self.__symbols = {_into_symbol(s) for s in symbols}

    def holds_for(self, model: Model) -> bool:
        return set(model.symbols(shown=True)).issubset(self.__symbols)


class SupersetOf(Assertion):
    def __init__(self, symbols: Set[Union[Symbol, str]]) -> None:
        self.__symbols = {_into_symbol(s) for s in symbols}

    def holds_for(self, model: Model) -> bool:
        return set(model.symbols(shown=True)).issuperset(self.__symbols)


class True_(Assertion):
    def holds_for(self, model: Model) -> bool:
        return True


class False_(Assertion):
    def holds_for(self, model: Model) -> bool:
        return False
