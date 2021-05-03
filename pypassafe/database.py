from typing import Optional

class DataBase:
    def __init__(self, path: str) -> None:
        pass

    def decrypt(self, master: str) -> None:
        self.master = master

    def encrypt(self, master: Optional[str] = None) -> None:
        pass

    def save(self, path: Optional[str] = None) -> None:
        pass

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
        raise ValueError("EncryptedDB should get path or existing DataBas")

    def decrypt(self, master: str) -> DecryptedDB:
        self.db.decrypt(master)
        return DecryptedDB(self.db)

    def save(self, path: Optional[str] = None) -> None:
        self.db.save(path)