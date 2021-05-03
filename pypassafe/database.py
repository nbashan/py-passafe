from typing import Optional, Callable, Any

class DataBase:
    def __init__(self, path: str) -> None:
        pass

    def decrypt(self, master: str) -> None:
        raise NotImplementedError()

    def encrypt(self, master: Optional[str] = None) -> None:
        raise NotImplementedError()

    def save(self, path: Optional[str] = None) -> None:
        raise NotImplementedError()

    def get(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> list[Any]:
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

    def encrypt(self, master: Optional[str] = None) -> 'EncryptedDB':
        self.db.encrypt(master)
        return EncryptedDB(db=self.db)

class EncryptedDB:
    def __init__(self, path: Optional[str] = None, db: Optional[DataBase] = None) -> None:
        if db is not None:
            self.db = db
            return
        if path is not None:
            self.db = DataBase(path)
            return
        raise ValueError("EncryptedDB should get path or existing DataBase")

    def decrypt(self, master: str) -> DecryptedDB:
        self.db.decrypt(master)
        return DecryptedDB(self.db)

    def save(self, path: Optional[str] = None) -> None:
        self.db.save(path)
