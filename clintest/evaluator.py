from enum import Enum
from typing import Optional

from .model import Model
from .utils import *

class Error():

    def __init__(self, info:str):
        self.info = info
    
    def __str__(self):
        return self.info


class Result():

    def __init__(self, is_success, errors):
        self.is_success = is_success
        self.errors = errors
    
    @classmethod
    def SUCCESS(cls):
        return cls(True, [])
    
    @classmethod
    def FAILURE(cls,errors):
        return cls(False, errors)
    
    def __str__(self):
        if self.is_success:
            return GREEN + "SUCCESS" + END_COLOR
        s = RED+ "FAIL"
        for e in self.errors:
            s+= "\n" + str(e)
        return s + END_COLOR       


class Evaluator:

    def __init__(self, description:str = ""):
        self.description=description
    
    def on_model(self, model: Model) -> Optional[Result]:
        pass

    def on_finish(self, *args) -> Result:
        pass

    def __str__(self):
        return self.description

