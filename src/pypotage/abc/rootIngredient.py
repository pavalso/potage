from typing import Any, Callable
from abc import abstractmethod

from ..utils import Chain, Priority
from .ingredient import Ingredient


class RootIngredient(Ingredient):

    priority = Priority.LAST

    resolve: Callable[..., Any]

    @abstractmethod
    def __call__(self, next = None) -> Any: ...
