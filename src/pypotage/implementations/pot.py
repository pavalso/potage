from typing import Generic, Type, TypeVar

from ..abc.potABC import PotABC
from ..abc.ingredientABC import IngredientABC
from ..utils import traverse_subclasses


_T = TypeVar("_T")

class Node(Generic[_T]):
    value: _T = None
    metadata: dict = None

    def __init__(self, value: _T = None):
        super().__init__()
        self.value = value
        self.metadata = {}


class Pot(PotABC):

    def __init__(self) -> None:
        self.contents: dict[Type, Node[list[IngredientABC]]] = {}

    def add(cls_or_self, ingredient):
        cls_or_self.contents \
            .setdefault(ingredient.formula.type, Node([])) \
            .value \
            .insert(0, ingredient)
        return ingredient

    def remove(cls_or_self, ingredient):
        cls_or_self.contents[ingredient.formula.type].value.remove(ingredient)

    def get(cls_or_self, formula):
        subclasses = traverse_subclasses(formula.type)
        subclasses.add(formula.type)

        included = set(cls_or_self.contents) \
            .intersection(subclasses)

        return [ingredient for node in [cls_or_self.contents[cls] for cls in included] for ingredient in node.value]

    def clear(cls_or_self):
        cls_or_self.contents.clear()
