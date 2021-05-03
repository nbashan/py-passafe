from database import DataBase
from typing import Optional, Callable, Any

class MyDataBase(DataBase):
    def __init__(self, path: str) -> None:
        super(MyDataBase, self).__init__(path)
        self.decrypted = False
        with open(self.path, 'rb') as file:
            self.data = file.read()

    def decrypt(self, master: str) -> None:
        raise NotImplementedError()

    def encrypt(self, master: Optional[str] = None) -> None:
        raise NotImplementedError()

    def save(self, path: Optional[str] = None) -> None:
        if self.decrypted:
            self.encrypt()
        if path is not None:
            self.path = path
        with open(self.path,'wb') as file:
            file.write(self.data)

    def get(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> list[Any]:
        raise NotImplementedError()

    def add(self, obj: Any) -> None:
        raise NotImplementedError()

    def update(self, predicate: Callable[[Any], Optional[Any]], count: Optional[int] = None) -> None:
        raise NotImplementedError()

    def remove(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> None:
        raise NotImplementedError()