
class MigrateableObject:
    @staticmethod
    def migrate(self, migrateable: "MigrateableObject") -> "MigrateableObject":
        raise NotImplementedError()

    @staticmethod
    def last(self) -> "MigrateableObject":
        raise NotImplementedError()

    def update_to_last(self) -> "MigrateableObject":
        return self.last().migrate(self)
