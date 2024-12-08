from ...abc.flavourABC import FlavourABC


class IdFlavour(FlavourABC):

    def __init__(self, id: str) -> None:
        self.id = id

    def apply_to(cls_or_self, ingredient):
        ingredient.formula.id = cls_or_self.id
