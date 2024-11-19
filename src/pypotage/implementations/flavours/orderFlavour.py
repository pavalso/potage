from ...abc.flavour import Flavour


class OrderFlavour(Flavour):

    def __init__(self, order: int) -> None:
        self.order = order

    def apply_to(self, meal):
        meal.formula.order = self.order
