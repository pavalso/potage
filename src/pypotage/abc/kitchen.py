from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Callable,
    Type,
    TypeVar,
    Any,
    Union
)

from .flavour import Flavour
from .ingredientProxy import IngredientProxy
from .packedMeal import PackedMeal


_Any = TypeVar("_Any")

class Kitchen(ABC):

    @abstractmethod
    def prepare(
            self,
            _f: Callable = None,
            *extra_flavours: list[Flavour]) -> Callable: ...

    @abstractmethod
    def cook(
            self,
            type: Type[_Any],
            id: str = None,
            proxies: list[IngredientProxy] = None) -> _Any: ...

    @abstractmethod
    def is_cooked(self, object: Any) -> bool: ...

    @abstractmethod
    def extract_ingredient(self, object: PackedMeal) -> IngredientProxy: ...

    @abstractmethod
    def is_present(self, object: Union[PackedMeal, Any]) -> bool: ...

    @abstractmethod
    def unpack(self, object: Union[PackedMeal, _Any]) -> _Any: ...
