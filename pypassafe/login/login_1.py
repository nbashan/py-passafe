from pypassafe.login import manager
from pypassafe.migrations import MigrateableObject


class Login1(MigrateableObject):
    def __init__(self, name: str, password: str) -> None:
        self.name = name
        self.password = password

    @staticmethod
    def migrate(migrateable: MigrateableObject) -> "Login1":
        assert isinstance(migrateable, Login1)
        return migrateable

    def update_to_last(self) -> MigrateableObject:
        return manager.Login.migrate(self)
