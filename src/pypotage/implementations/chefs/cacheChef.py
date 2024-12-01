from dataclasses import dataclass

from ...abc.chefABC import ChefABC
from ..waiters import CacheWaiter
from ...utils import Priority, traverse_subclasses


@dataclass
class CacheItem:
    checksum: int = 0


class CacheChef(ChefABC):

    priority = Priority.LAST

    checksums: dict[type, CacheItem] = {}

    @classmethod
    def prepare(cls_or_self, ingredient):
        _type = ingredient.formula.type
        
        if hasattr(_type, "__mro__"):
            affects = ingredient.formula.type.__mro__
        else:
            affects = [_type]

        for affected in affects:
            cls_or_self.checksums \
                .setdefault(affected, CacheItem()). \
                checksum += 1

        subclasses = traverse_subclasses(ingredient.formula.type)

        existing = {cls_or_self.checksums.get(cls) for cls in subclasses}
        existing.discard(None)

        for item in existing:
            item.checksum += 1

        return ingredient

    @classmethod
    def cook(cls_or_self, order):
        cache_waiter = order.add(CacheWaiter())

        og_take_out = order.take_out

        def __cache__(*args, **kwargs):
            cache_waiter.cache_item = cls_or_self.checksums.setdefault(cache_waiter.type, CacheItem())

            if cache_waiter.formula is None:
                cache_waiter.value = og_take_out(*args, **kwargs)
                cache_waiter.checksum = cache_waiter.cache_item.checksum
                return cache_waiter.value

            if cache_waiter.cache_item.checksum == cache_waiter.checksum:
                return cache_waiter.value

            cache_waiter.value = og_take_out(*args, **kwargs)
            cache_waiter.checksum = cache_waiter.cache_item.checksum
            return cache_waiter.value

        order.take_out = __cache__
