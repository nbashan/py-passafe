from typing import Type

from pypassafe.login import manager
from pypassafe.migrations import MigrateableObject
from .login_1 import Login1


class Login2(MigrateableObject):
    def __init__(self, name: str, password: str, url: str) -> None:
        self.name = name
        self.password = password
        self.url = url

    @staticmethod
    def migrate(migrateable: "MigrateableObject") -> "MigrateableObject":
        if isinstance(migrateable, Login2):
            return migrateable
        if not isinstance(migrateable, Login1):
            login1 = Login1.migrate(migrateable)
        else:
            login1 = migrateable
        return Login2(login1.name, login1.password, url="empty")

    @staticmethod
    def last() -> Type[MigrateableObject]:
        return manager.last()
