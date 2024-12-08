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

from .implementations.waiters.waiter import Waiter
from .implementations.pot import Pot
from .implementations.kitchen import Kitchen
from .implementations.chefLine import ChefLine
from .implementations.orders import Order
from .implementations.ingredient import Ingredient

from .implementations.chefs import DEFAULT_CHEFS
from .implementations.flavours import DEFAULT_FLAVOURS


lazy = flavours.LazyFlavour
no_call = flavours.NoCallFlavour
order = flavours.OrderFlavour
primary = flavours.PrimaryFlavour
id = flavours.IdFlavour
type = flavours.TypeFlavour

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
