
class MigrateableObject:
    def migrate(self, migrateable: "MigrateableObject") -> "MigrateableObject":
        raise NotImplementedError()

    def manager(self) -> "MigrationManager":
        raise NotImplementedError()

    def update_to_last(self) -> "MigrateableObject":
        return self.manager().last().migrate(self)

class MigrationManager:
    def last(self) -> MigrateableObject:
        raise NotImplementedError()

