from src import pypotage
import logging


if __name__ == "__main__":
    di = pypotage.cook(logging.Logger)

    print(di.is_present())

    @pypotage.prepare(
        pypotage.lazy)
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

    print(di.is_present(), di.take_out())

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

    print(di.is_present(), di.take_out())
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

        def do_uwu(self):
            self.logger.info("UwU")

    x = TestClass()
    x.do_uwu()

    @pypotage.prepare(
        pypotage.lazy,
        pypotage.primary
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

    x.do_uwu()
