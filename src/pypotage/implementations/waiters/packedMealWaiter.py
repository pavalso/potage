from ...abc.waiterABC import WaiterABC
from ...utils import Priority


class PackedMealWaiter(WaiterABC):

    priority = Priority.FIRST
