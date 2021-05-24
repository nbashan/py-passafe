from typing import Optional, Callable, Any, Type, List


class DataBase:
    def __init__(self, path: str) -> None:
        self.path = path

    def decrypt(self, master: str) -> None:
        raise NotImplementedError()

    def encrypt(self, master: Optional[str] = None) -> None:
        raise NotImplementedError()

    def save(self, path: Optional[str] = None) -> None:
        raise NotImplementedError()

    def get(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> List[Any]:
        raise NotImplementedError()

    def add(self, obj: Any) -> None:
        raise NotImplementedError()

    def update(self, predicate: Callable[[Any], Optional[Any]], count: Optional[int] = None) -> None:
        raise NotImplementedError()

    def remove(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> None:
        raise NotImplementedError()


class DecryptedDB:
    def __init__(self, db: DataBase) -> None:
        self.db = db

    def get(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> List[Any]:
        return self.db.get(predicate, count)

    def add(self, obj: Any) -> None:
        self.db.add(obj)

    def update(self, predicate: Callable[[Any], Optional[Any]], count: Optional[int] = None) -> None:
        return self.db.update(predicate, count)

    def remove(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> None:
        self.db.remove(predicate, count)


class EncryptedDB:
    def __init__(self, db_type: Optional[Type[DataBase]] = None, path: Optional[str] = None,
                 db: Optional[DataBase] = None) -> None:
        if db is not None:
            self.db = db
            return
        if path is not None and type is not None:
            self.db = db_type(path)
            return
        raise ValueError("EncryptedDB should get path and db type or existing DataBase")

    def decrypt(self, master: str, predicate: Callable[[DecryptedDB], None]) -> DecryptedDB:
        self.db.decrypt(master)
        predicate(DecryptedDB(self.db))
        self.db.encrypt(master)

    def save(self, path: Optional[str] = None) -> None:
        self.db.save(path)
