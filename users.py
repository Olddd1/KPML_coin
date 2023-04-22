import os.path
import sqlite3
import time
import traceback
from hashlib import sha256, md5

from blockchain_types import BlockObject


def create():
    connection = sqlite3.connect("users.sdb")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                      user_hash TEXT,
                      balance INT)""")
    connection.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS blockchain(
                      sender TEXT,
                      recipient TEXT,
                      amount INT,
                      hash TEXT,
                      prev_hash TEXT,
                      timestamp INT)""")
    connection.commit()

    amogus = {'hash': '3102454749e02249dc98633e3d77c2a3f573f1fd3a386d89faa5270396d29a7e',
              'prev_hash': 'b4c66a79ca5b060d0bb4038b77238c7b3fa781ddf4e7496e1cbfc937ba626e09',
              'from': 'John',
              'to': 'Bob',
              'amount': 100,
              'timestamp': 1681276701}

    cursor.execute(f"INSERT INTO blockchain VALUES ('{amogus.get('from')}', '{amogus.get('to')}', {amogus.get('amount')}, '{amogus.get('hash')}', '{amogus.get('prev_hash')}', {amogus.get('timestamp')})")
    connection.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS cheques(
                      cheque_hash TEXT,
                      recipient TEXT,
                      description TEXT,
                      amount INT,
                      status BOOL,
                      sender TEXT,
                      timestamp INT)""")
    connection.commit()

    cursor.close()
    connection.close()

class DataBase:
    def __init__(self):
        if not os.path.exists("users.sdb"):
            create()

        self.connection = sqlite3.connect("users.sdb")
        self.cursor = self.connection.cursor()

    def get_chain(self):
        self.cursor.execute("SELECT * FROM blockchain")
        return list(self.cursor.fetchall())

    def blockchain_update(self, block: BlockObject):
        try:
            self.cursor.execute(
                f"INSERT INTO "
                f"blockchain "
                f"VALUES "
                f"('{block.sender}', "
                f"'{block.recipient}',"
                f"{block.amount}, "
                f"'{block.hash}', "
                f"'{block.prev_hash}', "
                f"{block.timestamp})")
            self.connection.commit()
        except Exception as e:
            return {"error": traceback.format_exc()}

    def get_last_block(self):
        try:
            self.cursor.execute("SELECT * FROM blockchain ORDER BY timestamp DESC LIMIT 1;")
            block = self.cursor.fetchone()

            block = BlockObject(block)
            return block
        except:
            return {"error": ""}

    def user_create(self,
                    user_hash: str):
        try:
            self.cursor.execute(
                f"INSERT INTO users VALUES ('{user_hash}', 10000)")
            self.connection.commit()

            self.cursor.execute(f"SELECT * FROM users WHERE user_hash = '{user_hash}';")
            user = self.cursor.fetchone()
            return user
        except:
            return False

    def get_user(self, user_hash: str):
        self.cursor.execute(f"SELECT * FROM users WHERE user_hash = '{user_hash}';")
        user = self.cursor.fetchone()
        return user

    def update_user(self, user_hash, delta_amount):
        user = self.get_user(user_hash)
        amount = user[1] + delta_amount
        self.cursor.execute(f"UPDATE users SET balance={amount} WHERE user_hash='{user_hash}'")
        self.connection.commit()

    def create_cheque(self, description, amount, recipient):
        cheque_hash = md5()

        cheque_hash.update(str(amount).encode('utf-8'))
        cheque_hash.update(str(recipient).encode('utf-8'))
        cheque_hash.update(str(description).encode('utf-8'))
        cheque_hash.update(str(time.time()).encode('utf-8'))

        cheque_hash = cheque_hash.hexdigest()

        self.cursor.execute(f"INSERT INTO cheques VALUES('{cheque_hash}', '{recipient}', '{description}', {amount}, 0, '', 0)")
        self.connection.commit()
        
        return cheque_hash

    def get_cheque(self, cheque_hash):
        self.cursor.execute(f"SELECT * FROM cheques WHERE cheque_hash='{cheque_hash}'")
        return self.cursor.fetchone()

    def update_cheque(self, cheque_hash, sender):
        self.cursor.execute(f"UPDATE cheques SET sender='{sender}', timestamp={time.time()}, status=1 WHERE cheque_hash='{cheque_hash}'")
        self.connection.commit()

    def __repr__(self):
        return self.get_last_block()
    

description = "тестовый платёж"
amount = 100
recipient = "Bob"
