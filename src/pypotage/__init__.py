from typing import TypeAlias

from .utils import Priority

from . import abc
from .abc import (
    Formula,
    Flavour,
    Chef
)

from .implementations import (
    flavours,
    waiters,
    chefs,
    orders
)

from .implementations.waiters import Waiter
from .implementations.pot import Pot
from .implementations.kitchen import Kitchen
from .implementations.chefLine import ChefLine
from .implementations.orders import Order
from .implementations.ingredient import Ingredient

from .implementations.chefs import DEFAULT_CHEFS
from .implementations.flavours import DEFAULT_FLAVOURS


lazy: TypeAlias = flavours.LazyFlavour
no_call: TypeAlias = flavours.NoCallFlavour
order: TypeAlias = flavours.OrderFlavour
primary: TypeAlias = flavours.PrimaryFlavour
id: TypeAlias = flavours.IdFlavour
type: TypeAlias = flavours.TypeFlavour
singleton: TypeAlias = flavours.SingletonFlavour

def __prepare_kitchen() -> abc.Kitchen:
    return Kitchen()

kitchen_ = __prepare_kitchen()

prepare = kitchen_.prepare
cook = kitchen_.cook
get_order = kitchen_.get_order
is_cooked = kitchen_.is_cooked
is_prepared = kitchen_.is_prepared
unpack = kitchen_.unpack

__all__ = [
    "Flavour",
    "Waiter",
    "Formula",
    "Pot",
    "Kitchen",
    "Chef",
    "ChefLine",
    "chefs",
    "flavours",
    "waiters",
    "Priority",
    "lazy",
    "no_call",
    "order",
    "primary",
    "id",
    "type",
    "kitchen_",
    "prepare",
    "cook",
    "extract_ingredient",
    "is_cooked",
    "unpack",
    "abc",
    "orders",
    "Order",
    "DEFAULT_CHEFS",
    "DEFAULT_FLAVOURS",
    "Ingredient"
]
