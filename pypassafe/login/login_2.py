from pypassafe.login import manager
from pypassafe.migrations import MigrateableObject
from .login_1 import Login1

from typing import Optional


class Login2(MigrateableObject):
    def __init__(self, password: str, name: Optional[str] = None, url: Optional[str] = None) -> None:
        self.name = name
        self.password = password
        self.url = url

    @staticmethod
    def migrate(migrateable: MigrateableObject) -> "Login2":
        if isinstance(migrateable, Login2):
            return migrateable
        login1 = Login1.migrate(migrateable)
        return Login2(login1.name, login1.password, url="")

    def update_to_last(self) -> MigrateableObject:
        return manager.Login.migrate(self)
