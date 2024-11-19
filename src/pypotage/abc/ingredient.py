from abc import (
    ABC,
    abstractmethod
)
from typing import Any

from ..utils import Priorized, Chain


class Ingredient(ABC, Priorized):
    """Used to wrap avalue that can be resolved later."""

    @abstractmethod
    def __call__(self, next: Chain) -> Any:
        """Resolves the ingredient to its value.

        Returns:
            Any: The resolved value.

        Raises:
            StopReturn: If the ingredient should return a specific value.
        """
        ...
