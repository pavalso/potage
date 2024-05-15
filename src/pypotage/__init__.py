from . import ingredient as ingredients

from .pot import Pot
from .kitchen import (  # noqa: F401
    Kitchen,
    ChefLine,
    PackedMeal,
    Chef
)
from .decorators import (
    lazy,
    no_call,
    id,
    order,
    primary,
    type,
    ingredient
)

from . import defaultChefs as chefs


kitchen_ = Kitchen(
    Pot(),
    ChefLine([chefs.ListChef(), chefs.GenericChef()])
)

prepare = kitchen_.prepare
cook = kitchen_.cook

__all__ = [
    "prepare",
    "cook",
    "ingredients",
    "Pot",
    "Kitchen",
    "Chef",
    "PackedMeal",
    "ChefLine",
    "chefs",
    "lazy",
    "no_call",
    "id",
    "order",
    "primary",
    "type",
    "ingredient"
]
