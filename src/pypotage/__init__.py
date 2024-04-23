from . import ingredient as ingredients

from .pot import Pot
from .kitchen import Kitchen

from .chef import Chef
from .chefLine import ChefLine

from .chefsImpl import (
    ListChef,
    GenericChef
)


kitchen_ = Kitchen(
    Pot(),
    ChefLine([ListChef(), GenericChef()])
)

prepare = kitchen_.prepare
cook = kitchen_.cook


__all__ = [
    "prepare",
    "cook",
    "Chef",
    "ingredients",
    "Pot",
    "Kitchen",
    "ChefLine"
]
