from pypassafe.database import MyDataBase
from pypassafe.login import Login
import unittest
from unittest.mock import patch, mock_open, Mock

class TestMyDatabaseMethods(unittest.TestCase):
    def setUp(self):
        pass

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
    def test_encrypt_with_only_master(self, get_random_bytes: Mock) -> None:
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

    def test_encrypt_with_all_parameters(self) -> None:
        pass

    def test_encrypt_with_wrong_master(self) -> None:
        pass

    def test_encrypt_with_salt_size_out_of_range(self) -> None:
        pass

    def test_encrypt_with_loops_num_out_of_range(self) -> None:
        pass

if __name__ == '__main__':
    unittest.main()
