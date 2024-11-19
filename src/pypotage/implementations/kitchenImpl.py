from typing import (
    Any,
    Callable,
    Type,
    Union
)

from ..implementations.ingredients.rootIngredientImpl import RootIngredientImpl
from ..abc.ingredientProxy import IngredientProxy
from ..abc.flavour import Flavour
from ..abc.pot import Pot
from ..abc.kitchen import Kitchen
from ..abc.chefLine import ChefLine
from ..abc.chef import Chef
from ..abc.formula import Formula
from .potImpl import PotImpl
from .chefLineImpl import ChefLineImpl


class KitchenImpl(Kitchen):

    pot: Pot
    chef_line: ChefLine
    flavours: list[Flavour]

    def __init__(
            self,
            pot: Pot = None,
            chefs: Union[ChefLine, list[Type[Chef]]] = None,
            flavours: list[Flavour] = None) -> None:
        self.pot = pot or PotImpl()
        self.chef_line = chefs \
            if isinstance(chefs, ChefLine) \
            else ChefLineImpl(chefs)
        self.flavours = flavours or []

    def prepare(self, _f = None, *extra_flavours) -> Callable:
        def _wrapper(_f: Callable) -> Callable:
            meal = self.chef_line.prepare(
                ingredients=[RootIngredientImpl(_f)],
                flavours=[
                    *self.flavours,
                    *extra_flavours]
                )

            self.pot.add(meal)

            return _f

        called_decorator = _f is None  # @pypotage.prepare()

        if called_decorator:
            return _wrapper

        flavoured = isinstance(_f, Flavour) or \
            isinstance(_f, type) and issubclass(_f, Flavour)

        if flavoured:
            extra_flavours = [_f, *extra_flavours]
            return _wrapper

        return _wrapper(_f)

    def cook(self, type, id = None, proxies = None):
        if not (_t := getattr(type, "type", None)):
            _t = type

        order = _RootIngredientProxy(
            formula=Formula(type=_t, id=id),
            decorates=self.pot.get)

        cooked_order = self.chef_line.cook(order)
        cooked_order = IngredientProxy.from_list(cooked_order, proxies)

        ordered_proxies = IngredientProxy.sort(cooked_order)

        return self.chef_line.pack(ordered_proxies[0])

    def is_cooked(self, object) -> bool:
        return hasattr(object, "__ingredient__")

    def extract_ingredient(self, object) -> IngredientProxy:
        assert self.is_cooked(object), "Cannot retrieve IngredientProxy from a non-cooked object"

        return object.__ingredient__

    def is_present(self, object) -> bool:
        if not self.is_cooked(object):
            return True

        return object.__ingredient__.is_present()

    def unpack(self, object) -> Any:
        if not self.is_cooked(object):
            return object

        return object.__ingredient__.take_out()
