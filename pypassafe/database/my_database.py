from .database import DataBase
from pypassafe.migrations import MigrateableObject

from typing import Optional, Callable, Set
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
            self.data = set()
            return

        assert isinstance(self.data, bytes), "tries to decrypt when already decrypted"

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

    def encrypt(self, master: str, loops: int, salt_size: int) -> None:
        assert isinstance(self.data, set), "tries to encrypt when already encrypted"

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

    def get(self, predicate: Callable[[MigrateableObject], bool], count: Optional[int] = None) -> Set[MigrateableObject]:
        assert isinstance(self.data, set), "try to get while not decrypted"

        result = set()
        for obj in self.data:
            if (count is None or len(result) < count) and predicate(obj):
                result.add(obj)
        return result

    def add(self, obj: MigrateableObject) -> None:
        assert isinstance(self.data, set), "try to add while not decrypted"
        self.data.add(obj.update_to_last())

    def update(self, predicate: Callable[[MigrateableObject], Optional[MigrateableObject]], count: Optional[int] = None) -> None:
        assert isinstance(self.data, set), "try to update while not decrypted"

        new_data = set()
        for obj in self.data:
            if count is None or count > 0:
                x = predicate(obj)
                if x is None:
                    new_data.add(obj)
                else:
                    new_data.add(x)
                    if count is not None:
                        count -= 1
            else:
                new_data.add(obj)
        self.data = new_data

    def remove(self, predicate: Callable[[MigrateableObject], bool], count: Optional[int] = None) -> None:
        assert isinstance(self.data, set), "try to remove while not decrypted"

        new_data = set()
        for obj in self.data:
            if count is not None and count <= 0 or not predicate(obj):
                new_data.add(obj)
            elif count is not None:
                count -= 1
        self.data = new_data
