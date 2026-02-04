import sqlite3

from pkey import ProductKey, pkey_from_str

PKEYS_TABLE_NAME = "ProductKeys"

NEW_PKEYS = f"""
CREATE TABLE IF NOT EXISTS {PKEYS_TABLE_NAME} (
    pkey TEXT PRIMARY KEY
);
"""

INSERT_PKEY = f"""
INSERT INTO {PKEYS_TABLE_NAME} (pkey) VALUES (?);
"""

LIST_PKEYS = f"""
SELECT pkey FROM {PKEYS_TABLE_NAME}
"""


class ShitDB:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self) -> None:
        try:
            self.conn = sqlite3.connect("pkeys.db")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as ex:
            print(f"Database connection failed! {ex}")

    def disconnect(self):
        self.connection_check("disconnection")
        self.conn.close()

    def init(self) -> None:
        self.connection_check("initialization")
        self.cursor.execute(NEW_PKEYS)
        self.conn.commit()

    def add_key(self, key: ProductKey) -> None:
        self.connection_check("adding key")
        self.cursor.execute(INSERT_PKEY, (str(key),))
        self.conn.commit()

    def get_keys(self) -> list[ProductKey]:
        self.connection_check("key listing")
        self.cursor.execute(LIST_PKEYS)
        return [pkey_from_str(row[0]) for row in self.cursor.fetchall()]

    def has_key(self, key: ProductKey) -> bool:
        self.connection_check("checking key")
        self.cursor.execute(f"SELECT 1 FROM {PKEYS_TABLE_NAME} WHERE pkey = ? LIMIT 1", (str(key),))
        return self.cursor.fetchone() is not None

    def clear_keys(self) -> None:
        self.connection_check("clearing keys")
        self.cursor.execute(f"DELETE FROM {PKEYS_TABLE_NAME}")
        self.conn.commit()

    def connection_check(self, action: str) -> None:
        if self.conn is None or self.cursor is None:
            raise ShitDBNotConnectedError(f"Attempted {action} while not connected to database")


class ShitDBNotConnectedError(sqlite3.Error):
    pass
