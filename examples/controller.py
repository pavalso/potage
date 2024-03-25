from pypotage import bean, autowired

from .service import Service


@bean(lazy=True)
class Controller:

    def __init__(self):
        self.service = autowired(Service).get()

    def do_something(self):
        self.service.do_something()
