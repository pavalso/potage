from ...abc import Flavour as FlavourABC

from .forcedTypeFlavour import ForcedTypeFlavour
from .idFlavour import IdFlavour
from .lazyFlavour import LazyFlavour
from .noCallFlavour import NoCallFlavour
from .orderFlavour import OrderFlavour
from .primaryFlavour import PrimaryFlavour
from .typeFlavour import TypeFlavour
from .staticTypeCheckerFlavour import StaticTypeCheckerFlavour
from .singletonFlavour import SingletonFlavour


DEFAULT_FLAVOURS: list[FlavourABC] = [
    ForcedTypeFlavour,
    StaticTypeCheckerFlavour
]

__all__ = [
    "ForcedTypeFlavour",
    "IdFlavour",
    "LazyFlavour",
    "NoCallFlavour",
    "OrderFlavour",
    "PrimaryFlavour",
    "TypeFlavour",
    "SingletonFlavour",
    "StaticTypeCheckerFlavour",
    "DEFAULT_FLAVOURS"
]
