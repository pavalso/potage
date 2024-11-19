from .utils import Priority

from . import abc
from .abc import (
    Formula,
    Flavour,
    Chef
)

from .implementations import (
    flavours,
    ingredientProxies,
    chefs
)

from .implementations.ingredientProxies.ingredientProxyImpl import IngredientProxyImpl as IngredientProxy
from .implementations.potImpl import PotImpl as Pot
from .implementations.kitchenImpl import KitchenImpl as Kitchen
from .implementations.chefLineImpl import ChefLineImpl as ChefLine

DEFAULT_CHEFS: list[abc.Chef] = [
    chefs.ListChef,
    chefs.GenericChef,
    chefs.PackedMealChef
]
DEFAULT_FLAVOURS: list[abc.Chef] = [
    flavours.ForcedTypeFlavour,
    flavours.StaticTypeCheckerFlavour
]

lazy = flavours.LazyFlavour
no_call = flavours.NoCallFlavour
order = flavours.OrderFlavour
primary = flavours.PrimaryFlavour
id = flavours.IdFlavour
type = flavours.TypeFlavour

def __prepare_kitchen() -> abc.Kitchen:
    return Kitchen(
        pot=Pot(),
        chefs=ChefLine(DEFAULT_CHEFS),
        flavours=DEFAULT_FLAVOURS
    )

kitchen_ = __prepare_kitchen()

prepare = kitchen_.prepare
cook = kitchen_.cook
extract_ingredient = kitchen_.extract_ingredient
is_cooked = kitchen_.is_cooked
unpack = kitchen_.unpack

__all__ = [
    "Flavour",
    "IngredientProxy",
    "Formula",
    "Pot",
    "Kitchen",
    "Chef",
    "ChefLine",
    "chefs",
    "flavours",
    "ingredientProxies",
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
    "abc"
]
