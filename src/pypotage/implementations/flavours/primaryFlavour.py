from ...abc.flavourABC import FlavourABC


class PrimaryFlavour(FlavourABC):

    @classmethod
    def apply_to(cls_or_self, ingredient):
        ingredient.formula.primary = True
