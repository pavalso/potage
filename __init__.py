import logging

from src.pypotage import prepare, cook

from typing import Generic, TypeVar


_T = TypeVar("_T")

class Test(Generic[_T]):
    ...

@prepare(_id = 1)
def logger():
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(__name__)

@prepare(lazy=True)
def test() -> list[int]:
    return [1, 2, 3]

@prepare()
def ing() -> Test[logging.Logger]:
    return "sdas"

print(cook(logging.Logger, 1).take_out())
print(cook(list[int]).take_out())
print(cook(logging.Logger).take_out())
