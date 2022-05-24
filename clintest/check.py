from enum import Enum
import textwrap
from typing import Optional, Union
from xml.dom.pulldom import END_DOCUMENT
from clingo import Model, SolveResult, StatisticsMap
from .utils import *
NoneType = type(None)


class Error:

    def __init__(self, info:str):
        self.info = info
    
    def __str__(self):
        return self.info


class Result:

    def __init__(self, errors):
        self.errors = errors
    
    @property
    def is_success(self):
        return len(self.errors)==0

    @classmethod
    def success(cls):
        return cls([])
    
    @classmethod
    def failure(cls,errors):
        return cls(errors)
    
    def __str__(self):
        if self.is_success:
            return GREEN + "(SUCCESS)" + END_COLOR
        s = RED+ "(FAIL)"
        for e in self.errors:
            s+= "\n - " + str(e)
        return s + END_COLOR       


class Check:

    def __init__(self, description:str = ""):
        self.description=description
    
    def on_model(self, model: Model) -> Union[bool, NoneType]:
        pass

    def on_finish(self, result: SolveResult) -> NoneType:
        pass

    def on_statistics(self, step_statistics: StatisticsMap,
                        accumulated_statistics: StatisticsMap) -> NoneType:
        pass

    @property
    def result(self) -> Union[Result, NoneType]:
        return None

    @property
    def additional_info(self) -> str:
        return ""

    def __str__(self):
        s = CYAN + self.description + END_COLOR
        s += textwrap.indent(str(self.result), '\t') + "\n"
        s += self.additional_info

        return s

