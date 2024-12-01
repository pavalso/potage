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

from .flavourABC import FlavourABC
from .waiterABC import WaiterABC
from .mealABC import MealABC
from .orderABC import OrderABC
from .chefLineABC import ChefLineABC
from .potABC import PotABC


_Any = TypeVar("_Any")

class KitchenABC(ABC):

    chef_line: ChefLineABC
    pot: PotABC

    @abstractmethod
    def prepare(
            cls_or_self,
            func: Callable,
            *extra_flavours: list[FlavourABC]) -> Callable: ...

    @abstractmethod
    def cook(
            cls_or_self,
            type: Type[_Any],
            id: str = None,
            proxies: list[WaiterABC] = None) -> _Any: ...

    @abstractmethod
    def is_cooked(cls_or_self, object: Any) -> bool: ...

    @abstractmethod
    def get_order(cls_or_self, object: MealABC) -> OrderABC: ...

    @abstractmethod
    def is_prepared(cls_or_self, object: Union[MealABC, Any]) -> bool: ...

    @abstractmethod
    def unpack(cls_or_self, object: Union[MealABC, _Any]) -> _Any: ...
