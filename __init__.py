import abc

from src import pypotage


if __name__ == "__main__":
    class test(metaclass=abc.ABCMeta):
        @classmethod
        @abc.abstractmethod
        def test(self): ...

    @pypotage.prepare
    class test2(test):
        def test(self):
            return "test"

    print(pypotage.cook(test).take_out().test())
