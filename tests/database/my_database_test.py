from pypassafe.database import MyDataBase
from pypassafe.migrations import MigrateableObject
import unittest
from unittest.mock import patch, mock_open, Mock

class MockMigrateableObject(MigrateableObject):
    def __init__(self, name=""):
        self.called_update_to_last = 0
        self.name = name
    def update_to_last(self):
        self.called_update_to_last += 1
        return self

class TestMyDatabaseMethods(unittest.TestCase):
    def setUp(self):
        # mock open, I don't want to use the builtin open
        with patch("pypassafe.database.my_database.open") as open:
            open.side_effect = FileNotFoundError
            # create a new database to test CRUD 
            self.db = MyDataBase("mock")
            self.db.decrypt("master")
            assert isinstance(self.db.data, set), "when db is decrypted, its data's type should be a set"

        obj1 = MockMigrateableObject("name")
        obj2 = MockMigrateableObject("name")
        obj3 = MockMigrateableObject("nam3")
        self.db.add(obj1)
        self.db.add(obj2)
        self.db.add(obj3)

    @patch("pypassafe.database.my_database.open")
    def test_ctor_not_existing_file(self, open: Mock) -> None:
        path = "path/to/db"
        open.side_effect = FileNotFoundError

        db = MyDataBase(path)

        open.assert_called_once_with(path, 'rb')
        assert db.data is None, "db.data should be None because the file doesn't exist"

    def test_ctor_existing_file(self) -> None:
        with patch("pypassafe.database.my_database.open", mock_open(read_data=b'test_data')) as mock:
            path = "path/to/db"

            db = MyDataBase(path)

            mock.assert_called_once_with(path, 'rb')
            assert db.data == b'test_data', "MyDataBase didn't read the correct data from the file"

    @patch("pypassafe.database.my_database.get_random_bytes")
    def test_encrypt(self, get_random_bytes: Mock) -> None:
        return # wip
        db = MyDataBase("")
        db.data = set()
        master = "test_master"
        salt_size = 32
        loops = 1_000_000
        get_random_bytes.side_effect = lambda size: b'0' * size
        salt_bytes = salt_size.to_bytes(length=2, byteorder='little', signed=False)
        loops_bytes = loops.to_bytes(length=4, byteorder='little', signed=False)
        salt = b'0' * salt_size
        iv = b'0' * 16 # aes block size
        encrypted_data = b'\xb2\x08i\xc5\xfa\xd9U_\xe8\xf1\xa0\xa8\xb7\xbf\x88\x18'
        md5_hash = b''

        db.encrypt(master, loops, salt_size)

        get_random_bytes.assert_any_call(32) # check called for salt
        get_random_bytes.assert_any_call(16) # check called for iv
        assert isinstance(db.data, bytes), "data is not in bytes"
        # assert db.data[:16] == md5_hash, "md5 hash is wrong"
        assert salt_bytes == db.data[16:18], "wrong salt size in data"
        assert loops_bytes == db.data[18:22], "wrong loops size in data"
        assert salt == db.data[22:54], "wrong salt in data"
        assert iv == db.data[54:70], "wrong iv in data"
        print(db.data[70:])
        assert encrypted_data == db.data[70:], "wrong encrypted data in file"

    def test_encrypt_with_wrong_master(self) -> None:
        pass

    def test_encrypt_with_salt_size_out_of_range(self) -> None:
        pass

    def test_encrypt_with_loops_num_out_of_range(self) -> None:
        pass

    def test_add(self) -> None:
        obj = MockMigrateableObject()

        self.db.add(obj)

        assert isinstance(self.db.data, set), "after add, database's data's type should be a set"
        assert obj in self.db.data, "database should add obj"
        assert obj.called_update_to_last == 1, "should update to last"

    def test_get_without_count(self) -> None:
        result = self.db.get(lambda obj: hasattr(obj, "name") and obj.name == "name")

        assert len(result) == 2, "should be returned 2 objects"

    def test_get_with_count(self) -> None:
        result = self.db.get(lambda obj: hasattr(obj, "name") and obj.name == "name", 1)

        assert len(result) == 1, "should be returned 1 objects"

    def test_get_empty(self) -> None:
        result = self.db.get(lambda obj: False)

        assert len(result) == 0, "no objects should be returned"

    def test_get_with_count_greater_than_found(self) -> None:
        result = self.db.get(lambda obj: hasattr(obj, "name") and obj.name == "name", 3)

        assert len(result) == 2, "should be returned 2 objects"

    def test_update_without_count(self) -> None:
        def change_name(obj):
            if hasattr(obj, "name") and obj.name == "name":
                obj.name = "success"
                return obj

        self.db.update(change_name)

        result = self.db.get(lambda obj: hasattr(obj, "name") and obj.name == "success")
        assert len(result) == 2, "should update and return 2 objects"

    def test_update_with_count(self) -> None:
        def change_name(obj):
            if hasattr(obj, "name") and obj.name == "name":
                obj.name = "success"
                return obj

        self.db.update(change_name, 1)

        result = self.db.get(lambda obj: hasattr(obj, "name") and obj.name == "success")
        assert len(result) == 1, "should update and return 1 objects"

    def test_update_with_count_greater_than_found(self) -> None:
        def change_name(obj):
            if hasattr(obj, "name") and obj.name == "name":
                obj.name = "success"
                return obj

        self.db.update(change_name, 3)

        result = self.db.get(lambda obj: hasattr(obj, "name") and obj.name == "success")
        assert len(result) == 2, "should update and return 2 objects"

    def test_remove_without_count(self) -> None:
        find_name = lambda obj: hasattr(obj, "name") and obj.name == "name"

        self.db.remove(find_name)

        result = self.db.get(find_name)
        assert len(result) == 0, "should have removed all objects"

    def test_remove_with_count(self) -> None:
        find_name = lambda obj: hasattr(obj, "name") and obj.name == "name"

        self.db.remove(find_name, 1)

        result = self.db.get(find_name)
        assert len(result) == 1, "should keep 1 object"

    def test_remove_empty(self) -> None:
        self.db.remove(lambda obj: hasattr(obj, "name") and obj.name == "not found")

        assert isinstance(self.db.data, set)
        assert len(self.db.data) == 3, "should keep the data the same"

    def test_remove_with_count_greater_than_found(self) -> None:
        find_name = lambda obj: hasattr(obj, "name") and obj.name == "name"

        self.db.remove(find_name, 3)

        result = self.db.get(find_name)
        assert len(result) == 0, "should have removed all objects"

if __name__ == '__main__':
    unittest.main()
