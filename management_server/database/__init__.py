from calendar import c
import sqlite3
import os

DB_FILENAME = "db.db"

class Database:
    def __init__(self, supported_hashes):
        # Create the database if it doesnt exist yet
        if not self.check_db():
            self.create_db()
            for h in supported_hashes:
                self.add_hash_support(h)
        else:
            self.connect()

    def check_db(self):
        cwd = os.path.realpath(__file__)
        cwd = cwd[:cwd.find("__init__.py")]
        db_path = f'{cwd}/{DB_FILENAME}'
        return os.path.exists(db_path)

    def connect(self):
        cwd = os.path.realpath(__file__)
        cwd = cwd[:cwd.find("__init__.py")]
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
                  CREATE TABLE IF NOT EXISTS tokens 
                  ([token] TEXT PRIMARY KEY, [website_pubkey] TEXT, [used] BOOL)
                  ''')

        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS hashes 
                  ([hash_id] INTEGER PRIMARY KEY, [hash] TEXT, [hash_type] TEXT, [cracked] BOOL, [plaintext] TEXT )
                  ''')

        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS hash_types 
                  ([hash_id] INTEGER PRIMARY KEY, [hash_type] TEXT)
                  ''')

        self.conn.commit()

    def add_hash_support(self, hash_type):
        command = "INSERT INTO hash_types(hash_type) VALUES (?)"
        print("Adding new hash type to the database: ", hash_type)
        self.c.execute(command, (hash_type,))
        self.conn.commit()
        return True

    def add_hash(self, hash, type):
        # TODO check if hash exists, check if type is correct etc.
        command = 'INSERT INTO hashes(hash, hash_type, cracked, plaintext) VALUES (?, ?, ?, ?)'
        print("Adding new hash to the database: ", hash, type)
        self.c.execute(command, (hash, type, False, ""))
        self.conn.commit()
        return True

    def get_hashes(self):
        self.c.execute("SELECT * FROM hashes")
        data = self.c.fetchall()
        return data

if __name__ == "__main__":
    db = Database(['SHA256', 'MD5', 'Bcrypt'])
    print(db.get_hashes())
