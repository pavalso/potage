from src import pypotage

import logging


if __name__ == "__main__":
    class Proof:

        logger = pypotage.cook(logging.Logger)

        def test(self):
            print(self.logger)
            self.logger.info("Hello, World!")

    proof = Proof()

    @pypotage.prepare
    @pypotage.primary
    def prepare():
        print("Hello, World!")
        logger = logging.getLogger("Proof")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @pypotage.prepare
    @pypotage.lazy
    def prepare2() -> logging.Logger:
        print("Hello, World 2!")
        logger = logging.getLogger("Test")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    proof.test()
    proof.test()

    print(pypotage.cook(str).is_present())
