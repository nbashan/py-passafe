from .database import DataBase
from typing import Optional, Callable, Any, List
import pickle

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256, MD5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

MD5_SIZE = 16


class MyDataBase(DataBase):
    SALT_BYTES = 2
    LOOPS_BYTES = 4

    def __init__(self, path: str) -> None:
        super(MyDataBase, self).__init__(path)
        try:
            with open(self.path, 'rb') as file:
                self.data = file.read()
        except FileNotFoundError:
            self.data = None

    def decrypt(self, master: str) -> None:
        # when creating a new database, data is equal to None
        if self.data is None:
            self.data = list()
            return

        assert isinstance(self.data, bytes), "tries to decrypt when already decrypted"

        self.master = master
        offset = 0

        file_hash = self.data[offset:offset + MD5_SIZE]
        offset += MD5_SIZE
        data_hash = MD5.new(self.data[offset:]).digest()
        assert data_hash == file_hash, "file is corrupted"

        salt_size = int.from_bytes(self.data[offset:offset + self.SALT_BYTES], \
                byteorder='little', signed=False)
        offset += self.SALT_BYTES

        loops = int.from_bytes(self.data[offset:offset + self.LOOPS_BYTES], \
                byteorder='little', signed=False)
        offset += self.LOOPS_BYTES

        salt = self.data[offset:offset + salt_size]
        offset += salt_size
        key = PBKDF2(master, salt, 32, loops, hmac_hash_module=SHA256)

        iv = self.data[offset:offset + AES.block_size]
        offset += AES.block_size
        cipher = AES.new(key, AES.MODE_CBC, iv)

        encrypted = self.data[offset:]
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)

        self.data = pickle.loads(decrypted)

    def encrypt(self, master: Optional[str] = None, loops: int = 1000000, salt_size: int = 32) -> None:
        assert isinstance(self.data, list), "tries to encrypt when already encrypted"

        if master is None:
            master = self.master

        salt_size_bytes = salt_size.to_bytes(length=self.SALT_BYTES, byteorder='little', signed=False)
        loops_bytes = loops.to_bytes(length=self.LOOPS_BYTES, byteorder='little', signed=False)

        salt = get_random_bytes(salt_size)
        key = PBKDF2(master, salt, 32, loops, hmac_hash_module=SHA256)

        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        data_padded = pad(pickle.dumps(self.data), AES.block_size)

        self.data = salt_size_bytes + loops_bytes + salt + iv + cipher.encrypt(data_padded)

        md5_hash = MD5.new(self.data).digest()
        self.data = md5_hash + self.data

    def save(self, path: Optional[str] = None) -> None:
        assert isinstance(self.data, bytes), "tries to save decrypted data"

        if path is not None:
            self.path = path
        with open(self.path, 'wb') as file:
            file.write(self.data)

    def get(self, predicate: Callable[[Any], bool], count: Optional[int] = None) -> List[Any]:
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

