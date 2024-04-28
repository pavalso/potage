from src import pypotage


if __name__ == "__main__":
    @pypotage.prepare
    @pypotage.no_call
    class Test:
        def __init__(self):
            print("Test.__init__")

    @pypotage.prepare
    @pypotage.no_call
    @pypotage.lazy
    def test() -> str:
        print("test")
        return "test"

    t = pypotage.cook(Test).take_out()
    s = pypotage.cook(Test).take_out()

    print(t())
    print(s())
