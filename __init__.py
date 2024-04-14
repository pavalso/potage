from src import pypotage


if __name__ == "__main__":
    @pypotage.prepare(no_call=True)
    class Test:
        def __init__(self):
            print("Test.__init__")

    @pypotage.prepare(no_call=True, lazy=True)
    def test() -> str:
        print("test")
        return "test"

    t = pypotage.cook(Test).take_out()
    s = pypotage.cook(str).take_out()

    print(t())
    print(s())
