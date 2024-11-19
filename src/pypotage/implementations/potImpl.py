from typing import Type

from ..abc.pot import Pot
from ..abc.meal import Meal
from ..utils import traverse_subclasses


class PotImpl(Pot):

    def __init__(self) -> None:
        self.contents: dict[Type, list[Meal]] = {}

    def add(self, meal: Meal) -> Meal:
        self.contents \
            .setdefault(meal.formula.type, []) \
            .insert(0, meal)
        return meal

    def remove(self, meal: Meal) -> None:
        self.contents[meal.formula.type].remove(meal)

    def get(self, type: type) -> list[Meal]:
        classes = [type]
        classes.extend(traverse_subclasses(type))

        meals = []

        for _class in classes:
            meal = self.contents.get(_class)

            if meal is None:
                continue

            meals.extend(meal)

        return meals
