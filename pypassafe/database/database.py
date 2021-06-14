from typing import Optional, Callable, Type, List, Any
from pypassafe.migrations import MigrateableObject


class DataBase:
    def __init__(self, path: str) -> None:
        self.path = path

    def decrypt(self, master: str) -> None:
        raise NotImplementedError()

    def encrypt(self, master: str, loops: int, salt_size: int) -> None:
        raise NotImplementedError()

    def save(self, path: Optional[str] = None) -> None:
        raise NotImplementedError()

    def get(self, predicate: Callable[[MigrateableObject], bool], count: Optional[int] = None) -> List[MigrateableObject]:
        raise NotImplementedError()

    def add(self, obj: MigrateableObject) -> None:
        raise NotImplementedError()

    def update(self, predicate: Callable[[MigrateableObject], Optional[MigrateableObject]], count: Optional[int] = None) -> None:
        raise NotImplementedError()

    def remove(self, predicate: Callable[[MigrateableObject], bool], count: Optional[int] = None) -> None:
        raise NotImplementedError()


class DecryptedDB:
    def __init__(self, db: DataBase) -> None:
        self.db = db

    def get(self, predicate: Callable[[MigrateableObject], bool], count: Optional[int] = None) -> List[MigrateableObject]:
        return self.db.get(predicate, count)

    def add(self, obj: MigrateableObject) -> None:
        self.db.add(obj)

    def update(self, predicate: Callable[[MigrateableObject], Optional[MigrateableObject]], count: Optional[int] = None) -> None:
        return self.db.update(predicate, count)

    def remove(self, predicate: Callable[[MigrateableObject], bool], count: Optional[int] = None) -> None:
        self.db.remove(predicate, count)


class EncryptedDB:
    def __init__(self, db_type: Optional[Type[DataBase]] = None, path: Optional[str] = None) -> None:
        if path is not None and type is not None:
            self.db = db_type(path)
            return
        raise ValueError("EncryptedDB should get path and db type or existing DataBase")

    def decrypt(self, master: str, predicate: Callable[[DecryptedDB], Any], loops: int = 1_000_000, salt_size: int = 32) -> Any:
        self.db.decrypt(master)
        result = predicate(DecryptedDB(self.db))
        self.db.encrypt(master, loops, salt_size)
        return result

    def save(self, path: Optional[str] = None) -> None:
        self.db.save(path)
