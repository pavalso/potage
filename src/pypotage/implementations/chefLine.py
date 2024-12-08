from ..abc.chefABC import ChefABC
from ..abc.chefLineABC import ChefLineABC
from ..abc.flavourABC import FlavourABC
from .meal import Meal
from .orders.order import Order
from .ingredient import Ingredient
from ..utils import Priorized


class ChefLine(ChefLineABC):

    def __init__(self, chefs: list[ChefABC] = None) -> None:
        self.chefs = chefs or []
        self.chefs = ChefABC.sort(self.chefs)

    def add(cls_or_self, chef) -> None:
        cls_or_self.chefs.append(chef)
        cls_or_self.chefs = ChefABC.sort(cls_or_self.chefs)

    def remove(cls_or_self, chef):
        cls_or_self.chefs.remove(chef)
        cls_or_self.chefs = ChefABC.sort(cls_or_self.chefs)

    def cook(cls_or_self, formula, func, waiters):
        order = Order(formula=formula, waiters=waiters, resolve=func)

        for chef in cls_or_self.chefs:
            order = chef.cook(order) or order

        order.waiters = Priorized.sort(order.waiters)

        return order

    def prepare(cls_or_self, formula, func, flavours):
        ingredient = Ingredient(resolve=func, formula=formula)
        flavours = FlavourABC.sort(flavours)

        for flavour in flavours:
            flavour.apply_to(ingredient)

        for chef in cls_or_self.chefs:
            chef.prepare(ingredient)

        return ingredient

    def pack(cls_or_self, order):
        return Meal(order)
