from ...abc.flavour import Flavour


class PrimaryFlavour(Flavour):

    @classmethod
    def apply_to(meal):
        meal.formula.primary = True
