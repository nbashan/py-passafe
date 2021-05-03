from database import DataBase
from typing import Optional, Callable, Any, Union

class MyDataBase(DataBase):
    def __init__(self, path: str) -> None:
        super(MyDataBase, self).__init__(path)
        self.decrypted = False
        with open(self.path, 'rb') as file:
            self.data: Union[list[Any], bytes] = file.read()

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
        return list(filter(predicate, self.data))

    def add(self, obj: Any) -> None:
        self.data.append(obj)

    def update(self, predicate: Callable[[Any], Optional[Any]], count: Optional[int] = None) -> None:
        ret = []
        for obj in self.data:
            x = predicate(obj)
            if x is None:
                ret.append(obj)
            else:
                ret.append(x)
        self.data = ret

    def remove(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> None:
        self.data = [obj for obj in self.data if not predicate(obj)]