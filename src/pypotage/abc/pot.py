from abc import (
    ABC,
    abstractmethod
)

from ..abc.meal import Meal


class Pot(ABC):

    @abstractmethod
    def add(self, meal: Meal) -> Meal: ...

    @abstractmethod
    def remove(self, meal: Meal) -> None: ...

    @abstractmethod
    def get(self, type: type) -> list[Meal]: ...
