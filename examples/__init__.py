from logging import Logger, Formatter, StreamHandler

from pypotage import bean, autowired

from .controller import Controller
from .repository import Repository


@bean
def logger_bean() -> Logger:
    logger = Logger("logger")
    logger.setLevel("INFO")
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

@bean
class SqlRepository(Repository):

    logger = autowired(Logger)

    def insert(self):
        self.logger.get().info("SqlRepository saved data")

def main():
    controller = autowired(Controller).get()
    controller.do_something()
