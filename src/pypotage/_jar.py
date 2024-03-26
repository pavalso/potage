from typing import Callable, Type, TypeVar
from functools import cache, partial
from math import inf

from ._bean import _Bean, _BeanProxy
from .utils import traverse_subclasses


_B = TypeVar("_B")

class _Jar:

    _beans: dict[Type, list[_Bean]] = { }

    @classmethod
    def create(cls, func: Callable, **kwargs) -> _Bean:
        return _Bean(_c = cache(func), **kwargs)

    @classmethod
    def add(cls, _bean: _Bean) -> _Bean:
        (_l := cls._beans.setdefault(_bean.type, [])).append(_bean)
        list.sort(_l, key=lambda _b: _b.priority)
        return _bean

    @classmethod
    def get(cls, _type: Type) -> _Bean:
        classes = [_type]
        classes.extend(traverse_subclasses(_type))

        _beans = [ ]

        for _type in classes:
            if (_bean := cls._beans.get(_type)) is not None:
                _beans.extend(_bean)

        list.sort(_beans, key=lambda _bean: _bean.priority)

        return _beans

    @classmethod
    def bean(cls, _f: _B = None,
            /, lazy: bool = False, order: int = inf, primary: bool = False) -> _B:
        def _wrapper(_f) -> _Bean:
            _bean = cls.create(_f, lazy = lazy, order = order, primary = primary)
            cls.add(_bean)
            return _f
        return _wrapper(_f) if _f is not None else _wrapper

    @classmethod
    def autowired(cls, _type: _B) -> _BeanProxy[_B]:
        _t = _type if isinstance(_type, type) else _type.type

        return _BeanProxy(_f = partial(cls.get, _t))

jar = _Jar()
 