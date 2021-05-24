from unittest import main, TestCase
from pypassafe.login import Login
from pypassafe.login.login_1 import Login1
from pypassafe.login.login_2 import Login2

class TestLoginMigrations(TestCase):
    def test_login_is_last(self) -> None:
        assert Login == Login2, "Last login should be Login2"

    def test_login1_update_to_last(self) -> None:
        login1 = Login1("test", "test")

        last = login1.update_to_last()

        assert isinstance(last, Login), "Login1 doesn't update to last login"

    def test_login2_update_to_last(self) -> None:
        login2 = Login2("test", "test", "test")

        last = login2.update_to_last()

        assert isinstance(last, Login), "Login2 doesn't update to last login"

    def test_login1_migrate_to_login1(self) -> None:
        login1 = Login1("test1", "test1")

        migrated = Login1.migrate(login1)

        assert login1 is migrated, "Login1 should migrated to Login1"

    def test_login1_migrate_to_login2(self) -> None:
        login1 = Login1("test1", "test1")

        migrated = Login2.migrate(login1)

        assert migrated.name == "test1", "Name changed when Login1 migrated to Login2"
        assert migrated.password == "test1", "Password changed when Login1 migrated to Login2"
        assert migrated.url == "", "Url wasn't empty string when Login1 migrated to Login2"

    def test_login2_migrate_to_login2(self) -> None:
        login2 = Login2("test2", "test2", "test2")

        migrated = Login2.migrate(login2)

        assert login2 is migrated, "Login2 should migrated to Login2"


if __name__ == "__main__":
    main()

