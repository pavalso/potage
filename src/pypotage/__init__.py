from . import ingredient as ingredients

from .pot import Pot
from .kitchen import Kitchen

from .chef import Chef
from . import chefsImpl as chefs
from .chefLine import ChefLine


kitchen_ = Kitchen(
    Pot(),
    ChefLine([chefs.ListChef(), chefs.GenericChef()])
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
    "ChefLine",
    "chefs",
]
