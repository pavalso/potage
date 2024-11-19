from ...abc.ingredientProxy import IngredientProxy
from ...abc.chef import Chef
from .genericChef import GenericChef
from ..ingredientProxies import PackedMealIngredientProxy


class PackedMealChef(Chef):
    
    priority = Chef.before(GenericChef)

    @staticmethod
    def cook(line: IngredientProxy):
        if not getattr(line.formula.type, "__origin__", None) == IngredientProxy:
            return line
        line.formula.type = line.formula.type.__args__[0]
        return PackedMealIngredientProxy(formula=line.formula, decorates=line)
