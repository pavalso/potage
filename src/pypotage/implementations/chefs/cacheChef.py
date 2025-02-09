from dataclasses import dataclass

from ...abc.chefABC import ChefABC
from ..waiters import CacheWaiter
from ...utils import Priority, traverse_subclasses


@dataclass(unsafe_hash=True)
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

        def __return__():
            if cache_waiter.exception is True:
                raise cache_waiter.value
            return cache_waiter.value

        def __cache__(*args, **kwargs):
            if cache_waiter.cache_item is not None \
                    and cache_waiter.cache_item.checksum == cache_waiter.checksum \
                    and not cache_waiter.exception:
                return __return__()

            try:
                cache_waiter.value = og_take_out()
                cache_waiter.exception = False
            except Exception as e:
                cache_waiter.value = e
                cache_waiter.exception = True
            cache_waiter.cache_item = cls_or_self.checksums.setdefault(cache_waiter.type, CacheItem())
            cache_waiter.checksum = cache_waiter.cache_item.checksum
            return __return__()

        order.take_out = __cache__
