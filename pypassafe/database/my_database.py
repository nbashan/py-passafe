from .database import DataBase
from typing import Optional, Callable, Any, List
import pickle

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class MyDataBase(DataBase):
    SALT_SIZE = 32

    def __init__(self, path: str) -> None:
        super(MyDataBase, self).__init__(path)
        try:
            with open(self.path, 'rb') as file:
                self.data = file.read()
        except FileNotFoundError:
            self.data = list()

    def decrypt(self, master: str) -> None:
        if self.__is_decrypted():
            return

        self.master = master

        salt = self.data[AES.block_size:AES.block_size + MyDataBase.SALT_SIZE]
        key = self.__generate_key(self.master, salt) # type: ignore

        iv = self.data[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv) # type: ignore

        encrypted = self.data[AES.block_size + MyDataBase.SALT_SIZE:]
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size) # type: ignore

        self.data = pickle.loads(decrypted)

    def encrypt(self, master: Optional[str] = None) -> None:
        if not self.__is_decrypted():
            return

        if master is None:
            master = self.master
        salt = get_random_bytes(MyDataBase.SALT_SIZE)
        key = self.__generate_key(master, salt)

        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        data_padded = pad(pickle.dumps(self.data), AES.block_size)
        self.data = iv + salt + cipher.encrypt(data_padded)

    def save(self, path: Optional[str] = None) -> None:
        if self.__is_decrypted():
            self.encrypt()
        if path is not None:
            self.path = path
        with open(self.path, 'wb') as file:
            file.write(self.data) # type: ignore

    def get(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> List[Any]:
        return list(filter(predicate, self.data))

    def add(self, obj: Any) -> None:
        self.data.append(obj) # type: ignore

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

    def __is_decrypted(self) -> bool:
        return isinstance(self.data, list)

    @staticmethod
    def __generate_key(password: str, salt: bytes) -> bytes:
        return PBKDF2(password, salt, 32, 1000000, hmac_hash_module=SHA256)
