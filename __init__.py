from typing import Generic, TypeVar
import src.pypotage as pypotage

import logging
import traceback


_T = TypeVar("_T")
class Test(Generic[_T]): ...


@pypotage.prepare(
    pypotage.no_call
)
def test() -> pypotage.Kitchen:
    return pypotage.kitchen_

if __name__ == "__main__":
    print(pypotage.cook(pypotage.IngredientProxy[logging.Logger]))

    di = pypotage.cook(logging.Logger)

    print(pypotage.is_cooked(di))
    print(pypotage.is_cooked(logging.Logger))

    print(pypotage.extract_ingredient(di))

    try:
        print(pypotage.extract_ingredient(1))
        exit(-1)
    except:
        traceback.print_exc()

    ingr = pypotage.extract_ingredient(di)
    print(ingr.is_present())
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

    print(ingr.is_present())
    print(type(di))
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

    @pypotage.prepare
    def test():
        return 1

    print(pypotage.cook(int))
    
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

    print(pypotage.cook(Test[int]), pypotage.cook(list[Test]), pypotage.cook(list[Test[str]]))

    cook = pypotage.cook(Test[int])
    print(type(pypotage.unpack(cook)), type(cook))


from objproxies import ObjectProxy, CallbackProxy

class DynamicMeta(type):
    def __call__(self, *args, **kwds):
        instance = super().__call__(*args, **kwds)

        class UniqueMeta(type):
            def __repr__(_):
                return repr(instance.__class__)

        # Dynamically create a new class with UniqueMeta as its metaclass
        class __Wrap__(ObjectProxy, metaclass=UniqueMeta): ...

        return __Wrap__(instance)

class PackedMeal(CallbackProxy, metaclass = DynamicMeta):
    ...

def func():
    return "Hello"

a = PackedMeal(func) 

print(type(a))

import timeit

setup_code = """
from objproxies import CallbackProxy

class DynamicMeta(type):
    def __call__(self, *args, **kwds):
        class UniqueMeta(type):
            def __repr__(_):
                return repr(self)

        class Test(CallbackProxy, metaclass=UniqueMeta): ...

        instance = super().__call__(*args, **kwds)
        return Test(lambda: instance)

class OutTest(metaclass=DynamicMeta):
    def do_test(self):
        return "Doing a test!"

"""

check_code = """
class OutTest():
    def do_test(self):
        return "Doing a test!"

"""

no_meta_code = """
from objproxies import CallbackProxy

class _OutTest:
    def do_test(self):
        return "Doing a test!"

class OutTest(CallbackProxy):
    def __init__(self):
        instance = _OutTest()
        super().__init__(lambda: instance)

"""

test_code = """
a = OutTest()
a.do_test()
"""

# Measure the time taken to create an instance and call a method
execution_time = timeit.timeit(test_code, setup=setup_code, number=10000)
print(f"Execution time for 1000 iterations: {execution_time} seconds")

# Measure the time taken to create an instance and call a method
execution_time = timeit.timeit(test_code, setup=check_code, number=10000)
print(f"Execution time for 1000 iterations: {execution_time} seconds")

# Measure the time taken to create an instance and call a method
execution_time = timeit.timeit(test_code, setup=no_meta_code, number=10000)
print(f"Execution time for 1000 iterations: {execution_time} seconds")
