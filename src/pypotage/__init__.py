from . import ingredient as ingredients

from .pot import Pot
from .kitchen import (  # noqa: F401
    Kitchen,
    ChefLine,
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

from . import chefsImpl as chefs


kitchen_ = Kitchen(
    Pot(),
    [chefs.ListChef(), chefs.GenericChef()]
)

prepare = kitchen_.prepare
cook = kitchen_.cook

__all__ = [
    "prepare",
    "cook",
    "ingredients",
    "Pot",
    "Kitchen",
    "Chef"
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
