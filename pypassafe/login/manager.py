from typing import Type

from pypassafe.migrations import MigrateableObject
from .login_2 import Login2


def last() -> Type[MigrateableObject]:
    return Login2
