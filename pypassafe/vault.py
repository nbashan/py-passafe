from .database import EncryptedDB, MyDataBase
from .login import Login

from typing import Optional, Set


class Vault:
    def __init__(self, path: str) -> None:
        self.db = EncryptedDB(db_type=MyDataBase, path=path)

    def get_password(self,
                     master: str,
                     name: Optional[str] = None,
                     url: Optional[str] = None,
                     count: Optional[int] = None) -> Set[str]:
        def get_correct_logins(obj):
            return isinstance(obj, Login) and \
                   (obj.url == url or url is None) and \
                   (obj.name == name or name is None)

        def get_password_from_db(db):
            return set(map(lambda login: login.password, db.get(get_correct_logins, count=count)))

        return self.db.decrypt(master=master, predicate=get_password_from_db)

    def get_url(self, master: str,
                name: Optional[str] = None,
                password: Optional[str] = None,
                count: Optional[int] = None) -> Set[str]:
        def get_correct_logins(obj):
            return isinstance(obj, Login) and \
                   (obj.password == password or password is None) and \
                   (obj.name == name or name is None)

        def get_url_from_db(db):
            return set(map(lambda login: login.url, db.get(get_correct_logins, count=count)))

        return self.db.decrypt(master=master, predicate=get_url_from_db)

    def get_name(self, master: str,
                 url: Optional[str] = None,
                 password: Optional[str] = None,
                 count: Optional[int] = None) -> Set[str]:
        def get_correct_logins(obj):
            return isinstance(obj, Login) and \
                   (obj.password == password or password is None) and \
                   (obj.url == url or url is None)

        def get_name_from_db(db):
            return set(map(lambda login: login.name, db.get(get_correct_logins, count=count)))

        return self.db.decrypt(master=master, predicate=get_name_from_db)

    def get_login(self,
            master: str,
            password: Optional[str] = None,
            name: Optional[str] = None,
            url: Optional[str] = None,
            count: Optional[int] = None) -> Set[Login]:

        def get_correct_logins(obj):
            return isinstance(obj, Login) and \
                    (obj.password == password or password is None) and \
                    (obj.url == url or url is None) and \
                    (obj.name == name or name is None)
        def get_login_from_db(db):
            return db.get(get_correct_logins, count=count)

        return self.db.decrypt(master=master, predicate=get_login_from_db)

    def add_login(self,
                  password: str,
                  master: str,
                  name: Optional[str] = None,
                  url: Optional[str] = None) -> None:
        if name is None and url is None:
            raise ValueError("name or url must be given")

        def add_login_to_db(db):
            db.add(Login(name=name, url=url, password=password))

        self.db.decrypt(master=master, predicate=add_login_to_db)
        self.db.save()

    def set_login(self,
                  master: str,
                  password: Optional[str] = None,
                  url: Optional[str] = None,
                  name: Optional[str] = None,
                  new_password: Optional[str] = None,
                  new_url: Optional[str] = None,
                  new_name: Optional[str] = None,
                  count: Optional[int] = None) -> None:

        def get_correct_logins(obj):
            if isinstance(obj, Login) and \
                   (obj.password == password or password is None) and \
                   (obj.url == url or url is None) and \
                   (obj.name == name or name is None):
                if new_password is not None:
                    obj.password  = new_password
                if new_name is not None:
                    obj.name = new_name
                if new_url is not None:
                    obj.url = url

                return obj
            return None

        def update_login(db):
            db.update(predicate=get_correct_logins,count=count)

        return self.db.decrypt(master=master,predicate=update_login)
