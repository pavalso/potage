from ...abc.flavour import Flavour


class IdFlavour(Flavour):

    def __init__(self, id: str) -> None:
        self.id = id

    def apply_to(self, meal):
        meal.formula.id = self.id
