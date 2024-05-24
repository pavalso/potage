from . import ingredient as ingredients
from . import utils

from .utils import Priority

from . import flavours

from . import defaultChefs as chefs

from .ingredient import (
    Ingredient,
    Flavour,
    IngredientProxy,
    IngredientData
)
from .pot import Pot
from .kitchen import (  # noqa: F401
    Kitchen,
    ChefLine,
    Chef
)

lazy = flavours.LazyFlavour
no_call = flavours.NoCallFlavour
order = flavours.OrderFlavour
primary = flavours.PrimaryFlavour
id = flavours.IdFlavour
type = flavours.TypeFlavour

kitchen_ = Kitchen(
    pot=Pot(),
    chefs=ChefLine([chefs.ListChef(), chefs.GenericChef()])
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
    "ChefLine",
    "chefs",
    "lazy",
    "no_call",
    "id",
    "order",
    "primary",
    "type",
    "Ingredient",
    "utils",
    "Flavour",
    "IngredientProxy",
    "Priority",
    "IngredientData",
    "flavours"
]
