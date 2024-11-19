from abc import (
    ABC,
    abstractmethod
)

from ..utils import Priorized
from ..abc.meal import Meal


class Flavour(ABC, Priorized):

    @classmethod
    @abstractmethod
    def apply_to(cls, meal: Meal) -> None: ...
