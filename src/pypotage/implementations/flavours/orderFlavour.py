from ...abc.flavourABC import FlavourABC


class OrderFlavour(FlavourABC):

    def __init__(self, order: int) -> None:
        self.order = order

    def apply_to(cls_or_self, ingredient):
        ingredient.formula.order = cls_or_self.order
