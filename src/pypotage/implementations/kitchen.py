from typing import (
    Callable,
    Type,
    Union
)

from ..abc.flavourABC import FlavourABC
from ..abc.kitchenABC import KitchenABC
from ..abc.chefLineABC import ChefLineABC
from ..abc.chefABC import ChefABC
from ..abc.formula import Formula
from ..abc.potABC import PotABC
from ..implementations.waiters.waiter import Waiter
from ..implementations.flavours import DEFAULT_FLAVOURS
from ..implementations.chefs import DEFAULT_CHEFS
from .pot import Pot
from .chefLine import ChefLine


class Kitchen(KitchenABC):

    pot: PotABC
    chef_line: ChefLineABC
    flavours: list[FlavourABC]

    def __init__(
            self,
            pot: PotABC = None,
            chefs: Union[ChefLineABC, list[Type[ChefABC]]] = None,
            flavours: list[FlavourABC] = None) -> None:
        self.pot = pot or Pot()
        chefs = chefs if chefs is not None else DEFAULT_CHEFS
        self.chef_line = chefs \
            if isinstance(chefs, ChefLineABC) \
            else ChefLine(chefs)
        self.flavours = flavours if flavours is not None else DEFAULT_FLAVOURS

    def prepare(cls_or_self, func = None, *extra_flavours):
        def _wrapper(_f: Callable) -> Callable:
            ingredient = cls_or_self.chef_line.prepare(
                formula=Formula(),
                flavours=[
                    *cls_or_self.flavours,
                    *extra_flavours],
                func=_f
                )

            cls_or_self.pot.add(ingredient)

            return _f

        called_decorator = func is None  # @pypotage.prepare()

        if called_decorator:
            return _wrapper

        flavoured = isinstance(func, FlavourABC) or \
            isinstance(func, type) and issubclass(func, FlavourABC)

        if flavoured:
            extra_flavours = [func, *extra_flavours]
            return _wrapper

        return _wrapper(func)

    def cook(cls_or_self, type, id = None, proxies = None):
        proxies = proxies or []
        
        if not (_t := getattr(type, "type", None)):
            _t = type

        cooked_order = cls_or_self.chef_line.cook(
            formula=Formula(type=_t, id=id),
            func=cls_or_self.pot.get,
            waiters=[*proxies, Waiter])

        return cls_or_self.chef_line.pack(cooked_order)

    def is_cooked(cls_or_self, object):
        return hasattr(object, "__order__") and \
            object.__order__ is not None

    def get_order(cls_or_self, object):
        assert cls_or_self.is_cooked(object), "Cannot retrieve IngredientProxy from a non-cooked object"

        return object.__order__

    def is_prepared(cls_or_self, object):
        if not cls_or_self.is_cooked(object):
            return True

        return object.__order__.is_prepared()

    def unpack(cls_or_self, object):
        if not cls_or_self.is_cooked(object):
            return object

        return object.__order__.take_out()
