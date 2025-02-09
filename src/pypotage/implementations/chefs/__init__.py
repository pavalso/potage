from ...abc import Chef as ChefABC

from .genericChef import GenericChef
from .listChef import ListChef
from .cacheChef import CacheChef


DEFAULT_CHEFS: list[ChefABC] = [
    ListChef,
    GenericChef,
    CacheChef
]

__all__ = [
    "GenericChef",
    "ListChef",
    "CacheChef",
    "AsyncChef",
    "DEFAULT_CHEFS"
]
