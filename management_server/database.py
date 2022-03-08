import sqlite3
import os
from config import DB_FILENAME, SUPPORTED_HASHES


class Database:
    def __init__(self, supported_hashes=SUPPORTED_HASHES):
        # Create the database if it doesnt exist yet
        if not self.check_db():
            self.create_db()
            for h in supported_hashes:
                print(supported_hashes)
                self.add_hash_support(h)
        else:
            self.connect()

    def check_db(self):
        cwd = os.path.realpath(__file__)
        cwd = cwd[:cwd.find("database.py")]
        db_path = f'{cwd}/{DB_FILENAME}'
        return os.path.exists(db_path)

    def connect(self):
        cwd = os.path.realpath(__file__)
        cwd = cwd[:cwd.find("database.py")]
        db_path = f'{cwd}/{DB_FILENAME}'
        self.conn = sqlite3.connect(db_path, check_same_thread=False) 
        self.c = self.conn.cursor()

    def create_db(self):
        self.connect()
        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS websites 
                  ([pubkey] TEXT PRIMARY KEY, [privkey] TEXT)
                  ''')

        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS tasks 
                  ([token] TEXT PRIMARY KEY, [used] BOOL, [hash_type] TEXT, [target] TEXT, [hash_id] INTEGER)
                  ''')

        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS hashes 
                  ([hash_id] INTEGER PRIMARY KEY, [hash] TEXT, [hash_type] TEXT, [cracked] BOOL, [plaintext] TEXT )
                  ''')

        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS hash_types 
                  ([hash_id] INTEGER PRIMARY KEY, [hash_type] TEXT, [bit_length] INT)
                  ''')

        self.conn.commit()

    def add_hash_support(self, hash_type):
        command = "INSERT INTO hash_types(hash_type, bit_length) VALUES (?, ?)"
        print("Adding new hash type to the database: ", hash_type)
        self.c.execute(command, (hash_type))
        self.conn.commit()
        return True

    def get_hash(self, hashId):
        self.c.execute(f"SELECT * FROM hashes WHERE hash_id={hashId}")
        data = self.c.fetchall()
        return data

    def add_hash(self, hash, type):
        # TODO check if hash exists, check if type is correct etc.
        command = 'INSERT INTO hashes(hash, hash_type, cracked, plaintext) VALUES (?, ?, ?, ?)'
        self.c.execute(command, (hash, type, False, ""))
        self.conn.commit()
        return True

    def set_hash_as_cracked(self, hashId, status, plaintext):
        self.c.execute("UPDATE hashes SET cracked = ?, plaintext = ? WHERE hash_id = ?", (status, plaintext, hashId))
        self.conn.commit()


    def get_all(self, table):
        self.c.execute(f"SELECT * FROM {table}")
        data = self.c.fetchall()
        return data

    def get_task(self, token):
        self.c.execute("SELECT * FROM tasks WHERE token = '%s'" % token)
        data = self.c.fetchall()
        return data   

    def set_new_task(self, token, hash_type, target, hashId):
        command = 'INSERT INTO tasks(token, used, hash_type, target, hash_id) VALUES (?, ?, ?, ?, ?)'
        self.c.execute(command, (token, False, hash_type, target, hashId))
        self.conn.commit()
        return True

    def update_token(self, token, status):
        self.c.execute("UPDATE tasks SET used = ? WHERE token = ?", (status, token))
        self.conn.commit()

    

if __name__ == "__main__":
    db = Database()
    print(db.get_all("hashes"))
