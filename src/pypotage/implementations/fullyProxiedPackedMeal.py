from objproxies import ObjectProxy

from .orders.order import PackedMeal


class DynamicMeta(type):
    def __call__(cls, *args, **kwds):
        instance = super().__call__(*args, **kwds)

        class UniqueMeta(type):
            def __repr__(_):
                return repr(instance.__class__)

        # Dynamically create a new class with UniqueMeta as its metaclass
        class __Wrap__(ObjectProxy, metaclass=UniqueMeta): ...

        return __Wrap__(instance)


class FullyProxiedPackedMeal(PackedMeal, metaclass = DynamicMeta): ...
