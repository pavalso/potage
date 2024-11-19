from ..abc.chef import Chef
from ..abc.ingredientProxy import IngredientProxy
from ..abc.packedMeal import PackedMeal
from ..abc.chefLine import ChefLine
from ..abc.formula import Formula
from ..abc.flavour import Flavour
from ..implementations.mealImpl import MealImpl


class ChefLineImpl(ChefLine):

    def __init__(self, chefs: list[Chef] = None) -> None:
        self.chefs = chefs or []
        self.chefs = Chef.sort(self.chefs)

    def add(self, chef) -> None:
        self.chefs.append(chef)
        self.chefs = Chef.sort(self.chefs)

    def remove(self, chef: Chef) -> Chef:
        return super().remove(chef)

    def cook(self, line) -> IngredientProxy:
        for _chef in self.chefs:
            line = _chef.cook(line)
        return line

    def prepare(self, ingredients, flavours):
        meal = MealImpl(ingredients=ingredients, formula=Formula())
        flavours = Flavour.sort(flavours)

        for flavour in flavours:
            flavour.apply_to(meal)

        for chef in self.chefs:
            chef.prepare(meal)

        return meal

    def pack(self, ingredient):
        packed = PackedMeal(ingredient)
        for _chef in self.chefs:
            packed = _chef.pack(packed)
        return packed
