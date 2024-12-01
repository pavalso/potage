from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable

from .formula import Formula


@dataclass
class IngredientABC(ABC):

    resolve: Callable
    formula: Formula

    @abstractmethod
    def take_out(cls_or_self) -> Any: ...
