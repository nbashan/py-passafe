from pypassafe.login import manager
from pypassafe.migrations import MigrateableObject


class Login1(MigrateableObject):
    def __init__(self, name: str, password: str) -> None:
        self.name = name
        self.password = password

    @staticmethod
    def migrate(migrateable: "MigrateableObject") -> "MigrateableObject":
        return migrateable

    @staticmethod
    def last() -> "MigrateableObject":
        return manager.last()
