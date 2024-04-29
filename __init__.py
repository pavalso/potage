from src import pypotage


if __name__ == "__main__":
    class Parent1:
        def __init__(self):
            print("Parent1.__init__")

        def test1(self):
            print("Parent1.test")

    class Parent2:
        def __init__(self):
            print("Parent2.__init__")

        def test2(self):
            print("Parent2.test")

    @pypotage.prepare
    class Child(Parent1, Parent2):
        def __init__(self):
            super().__init__()
            print("Child.__init__")

    print(pypotage.cook(Parent1).take_out())
    print(pypotage.cook(Parent2).take_out())
    print(pypotage.cook(Child).take_out())

    @pypotage.prepare(primary=True)
    class GrandChild(Child):
        def __init__(self):
            super().__init__()
            print("GrandChild.__init__")

    print(pypotage.cook(Parent1).take_out())
    print(pypotage.cook(Parent2).take_out())
    print(pypotage.cook(Child).take_out())
    print(pypotage.cook(GrandChild).take_out())
