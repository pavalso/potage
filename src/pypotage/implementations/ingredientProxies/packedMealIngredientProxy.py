from .ingredientProxyImpl import IngredientProxyImpl
from ...utils import Priority



class PackedMealIngredientProxy(IngredientProxyImpl):
    
    priority = Priority.FIRST
