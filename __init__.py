from src.pypotage import prepare, cook


if __name__ == "__main__":
    @prepare
    def bean1() -> str:
        return "bean1"

    @prepare
    def bean2() -> str:
        return "bean2"

    print(cook(list[str]).take_out())
