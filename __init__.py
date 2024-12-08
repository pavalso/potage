from typing import Generic, TypeVar
import src.pypotage as pypotage

import logging
import traceback


if __name__ == "__main__":
    di = pypotage.cook(logging.Logger)

    print(pypotage.is_cooked(di))
    print(pypotage.is_cooked(logging.Logger))

    print(pypotage.get_order(di))

    try:
        print(pypotage.get_order(1))
        exit(-1)
    except:
        traceback.print_exc()

    ingr = pypotage.get_order(di)
    print(ingr.is_prepared())
    print(type(di))

    @pypotage.prepare(
        pypotage.lazy,
        pypotage.no_call)
    def prepare2() -> logging.Logger:
        print("Hello, World 2!")
        logger = logging.getLogger("Test2")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    print(ingr.is_prepared())
    print(type(di))
    print("----------------")
    print(di)
    print("----------------")
    print(di)

    @pypotage.prepare(
        pypotage.lazy)
    def prepare1() -> logging.Logger:
        print("Hello, World 1!")
        logger = logging.getLogger("Test1")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    print(di)
    prepare1().info("Hello, World 1!")

    @pypotage.prepare(
        pypotage.lazy,
        pypotage.primary,
        pypotage.no_call,
        pypotage.order(1),
        pypotage.id("logger"),
        pypotage.type(logging.Logger)
    )
    class TestClass:

        logger = pypotage.cook(logging.Logger)

        def do_test(self):
            self.logger.info("Test")

    x = TestClass()
    x.do_test()

    @pypotage.prepare(
        pypotage.lazy
    )
    def prepare3() -> logging.Logger:
        print("Hello, World 3!")
        logger = logging.getLogger("Test3")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    x.do_test()

    ints = pypotage.cook(list[int])

    print(ints)

    @pypotage.prepare
    def test():
        return 1

    print(pypotage.cook(int))
    print(ints)
    print(ints)

    @pypotage.prepare
    def test():
        return 2

    print(ints)
    
    a = pypotage.cook(int)

    def test2(aLogger = pypotage.cook(logging.Logger)):
        print("Logging from %s" % aLogger)

    test2()

    @pypotage.prepare
    def test3():
        logger = logging.getLogger("Test4")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    test2()

    print(pypotage.cook(list[logging.Logger]))

    print(pypotage.cook(logging.Logger, "logger"))

    _T = TypeVar("_T")
    class Test(Generic[_T]): ...

    @pypotage.prepare(
        pypotage.type(Test[int])
    )
    def test1():
        return 1
    
    @pypotage.prepare(
        pypotage.type(Test[str])
    )
    def test1():
        return "1"

    @pypotage.prepare(
        pypotage.type(Test)
    )
    def test1():
        return True

    @pypotage.prepare(
        pypotage.type(Test[int])
    )
    def test1():
        return 2

    print(pypotage.cook(list[Test[int]]), pypotage.cook(list[Test]), pypotage.cook(list[Test[str]]))

    cook = pypotage.cook(Test[int])
    print(type(pypotage.unpack(cook)), type(cook))

    print("----------------")
    print(di)
    print("----------------")
    print(di)

    print(di)

    x.do_test()

    print(ints)
    j = pypotage.cook(int)
    print(j)
    
    @pypotage.prepare
    def test():
        return 3

    print(j)
    
    print(pypotage.cook(int))
    print(ints)
