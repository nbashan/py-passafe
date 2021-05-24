from typing import Type


class MigrateableObject:
    @staticmethod
    def migrate(migrateable: "MigrateableObject") -> "MigrateableObject":
        raise NotImplementedError()

    @staticmethod
    def last() -> Type["MigrateableObject"]:
        raise NotImplementedError()

    def update_to_last(self) -> "MigrateableObject":
        return self.last().migrate(self)
