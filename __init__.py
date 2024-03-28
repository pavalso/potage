import logging

from src.pypotage import prepare, cook

from typing import Generic, TypeVar


_T = TypeVar("_T")

class Test(Generic[_T]):
    ...

@prepare(_id = "logger")
def logger():
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(__name__)

@prepare(lazy=True)
def test() -> list[int]:
    return [1, 2, 3]

@prepare(lazy=True)
def ing() -> Test[logging.Logger]:
    return "sdas"

cook(logging.Logger, "logger").take_out().info("Hello, World!")
print(cook(list[int]).take_out().append(4))
print(cook(Test[str]).take_out())
