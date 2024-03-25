from logging import Logger

from pypotage import bean, autowired

from .repository import Repository


@bean(lazy=True)
class Service:

    def __init__(self):
        self.logger = autowired(Logger).get()
        self.repository = autowired(Repository).get()

    def do_something(self):
        self.logger.info("Service did something")
        self.repository.insert()
