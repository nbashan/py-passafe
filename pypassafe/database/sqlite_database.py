import sqlite3
from aifc import Error

from database import DataBase
from typing import Optional, Callable, Any


class SqliteDataBase(DataBase):
    def __init__(self, path: str) -> None:
        super(SqliteDataBase, self).__init__(path)
        self.decrypted = False
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.path)
            self.data = conn
        except Error as e:
            print(e)



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
        sql_create_login_table = f""" CREATE TABLE IF NOT EXISTS {obj.__name__} (
                                                                        id integer PRIMARY KEY,
                                                                    ); """
        # create tables
        if self.data is not None:
            # create projects table
            self.create_table(self.data, sql_create_login_table)
        else:
            print("Error! cannot create the database connection.")

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

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.data.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
