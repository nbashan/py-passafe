import sys
sys.path.append('pypassafe')

from pypassafe.database import EncryptedDB, MyDataBase
import unittest
from unittest.mock import mock_open

class TestMyDatabaseMethods(unittest.TestCase):
    def setUp(self):
        self.mock_open_not_found = mock_open()
        self.mock_open_not_found.side_effect = FileNotFoundError

    def test_ctor(self):
        pass

    def test_decrypt(self):
        pass

    def test_encrypt(self):
        pass

    def test_save(self):
        pass

    def test_get(self):
        pass

    def test_update(self):
        pass

    def test_remove(self):
        pass

    def test_is_decrypted(self):
        pass

    def test_data_to_json(self):
        pass


    def test_set_data_from_json(self):
        pass

    def test_encode_to_json(self):
        pass

    def test_decode_from_json(self):
        pass

    def test_pad(self):
        pass

    def test_unpad(self):
        pass

    def test_generate_key(self):
        pass


if __name__ == '__main__':
    unittest.main()
