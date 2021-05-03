from .database import DataBase
from typing import Optional, Callable, Any, Union
import json

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

class MyDataBase(DataBase):
    SALT_SIZE = 32

    def __init__(self, path: str) -> None:
        super(MyDataBase, self).__init__(path)
        self.master = ""
        with open(self.path, 'rb') as file:
            self.data: Union[list[Any], bytes] = file.read()

    def decrypt(self, master: str) -> None:
        if self.__is_decrypted():
            return

        iv = self.data[:AES.block_size]
        salt = self.data[AES.block_size:MyDataBase.SALT_SIZE]
        encrypted = self.data[AES.block_size + MyDataBase.SALT_SIZE:]
        key = self.__generate_key(master, salt)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted).decode()

        self.__set_data_from_json(self.__unpad(decrypted))

    def encrypt(self, master: Optional[str] = None) -> None:
        if not self.__is_decrypted():
            return

        if master is None:
            master = self.master
        salt = get_random_bytes(MyDataBase.SALT_SIZE)
        key = self.__generate_key(master, salt)

        json_padded = self.__pad(self.__data_to_json())

        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        self.data = iv + salt + cipher.encrypt(json_padded.encode())

    def save(self, path: Optional[str] = None) -> None:
        if self.__is_decrypted():
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

    def __is_decrypted(self) -> bool:
        return isinstance(self.data, list)

    def __data_to_json(self) -> str:
        json_list = map(lambda obj: self.__encode_to_json(obj), self.data)
        json_data = ",\n".join(json_list)
        return json_data

    def __set_data_from_json(self, json_data: str) -> None:
        data = json_data.split(",\n")
        self.data = list(map(lambda obj: self.__decode_from_json(obj), data))

    @staticmethod
    def __encode_to_json(obj: Any) -> str:
        result = obj.__dict__
        result["@@type@@"] = obj.__name__
        return json.dumps(result)

    @staticmethod
    def __decode_from_json(encoded: str) -> Any:
        result = json.loads(encoded)
        type_name = result["@@type@@"]
        del result["@@type@@"]

        type = globals()[type_name]
        return type(dict=result)

    @staticmethod
    def __pad(data: str) -> str:
        return data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)

    @staticmethod
    def __unpad(padded: str) -> str:
        return padded[:-ord(padded[len(padded)-1:])]

    @staticmethod
    def __generate_key(password: str, salt: bytes) -> bytes:
        return PBKDF2(password, salt, 32, 1000000, hmac_hash_module=SHA256)

