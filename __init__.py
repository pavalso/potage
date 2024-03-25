from pypotage import bean

from examples import main, SqlRepository


@bean(primary=True)
class MockRepository(SqlRepository):

    def insert(self):
        self.logger.get().info("MockRepository saved data")
        super().insert()

if __name__ == "__main__":
    main()
