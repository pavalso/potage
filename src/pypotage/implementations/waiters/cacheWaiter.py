from ...abc.waiterABC import WaiterABC
from ...utils import Priority


class CacheWaiter(WaiterABC):
    
    priority = Priority.LAST

    @property
    def type(self):
        return self.formula.type if self.formula else None

    def __init__(self, formula=None):
        self.formula = formula
        self.value = None
        self.checksum = 0
        self.cache_item = None

    def serve(cls_or_self, formula, ingredients):
        cls_or_self.formula = formula
        return ingredients
