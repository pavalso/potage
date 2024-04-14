from src import pypotage


if __name__ == "__main__":
    import typing

    T = typing.TypeVar("T")
    K = typing.TypeVar("K")

    class MyGeneric(typing.Generic[T, K]):
        ...

    class MyGenericSubclass(MyGeneric[T, K]):
        ...

    pypotage.prepare(MyGenericSubclass[typing.Generic[T], str])

    print(pypotage.cook(list[MyGeneric[typing.Generic[T], str]]).take_out())
