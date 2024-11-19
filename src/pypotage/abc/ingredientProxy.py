from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Any,
    Generic,
    TypeVar
)
from dataclasses import dataclass

from .formula import Formula
from ..utils import Priorized, Chain


_B = TypeVar("_B")

@dataclass
class IngredientProxyChain(Chain):

    __formula__: Formula

    def __call__(self) -> Any:
        return super().__call__(formula=self.__formula__)

class IngredientProxy(ABC, Generic[_B], Priorized):

    @abstractmethod
    def is_present(self) -> bool: ...

    @abstractmethod
    def __call__(self, formula: Formula, next: IngredientProxyChain) -> _B: ...
