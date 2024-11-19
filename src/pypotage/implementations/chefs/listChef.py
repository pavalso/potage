from ...abc.chef import Chef
from ...abc.ingredientProxy import IngredientProxy
from .genericChef import GenericChef
from ..ingredientProxies import ListIngredientProxy


class ListChef(Chef):

    priority = Chef.before(GenericChef)

    @staticmethod
    def cook(line: IngredientProxy) -> IngredientProxy:
        if not getattr(line.formula.type, "__origin__", None) == list:
            return line
        line.formula.type = line.formula.type.__args__[0]
        return ListIngredientProxy(formula=line.formula, decorates=line)
