import random
from database import Database
from uuid import uuid4
import hashlib

class WorkDispatcher:
    def __init__(self):
        self.db = Database()


    def get_hashtype_info(self, hashtype):
        data = self.db.get_all("hash_types")
        for h in data:
            if h[1] == hashtype:
                return h[2]


    def hash(self, data, hashtype):
        if hashtype == "MD5":
            return hashlib.md5(data).hexdigest()
        elif hashtype == "SHA256":
            return hashlib.sha256(data).hexdigest() 


    def hex_to_binary(self, data, fill_length):
        return bin(int(data, 16))[2:].zfill(fill_length)


    def select_task(self, hashes, difficulty=20):
        hashId, h, hashtype, cracked, plaintext = random.choice(hashes)
        hash_length = self.get_hashtype_info(hashtype)  
        hash_binary = bin(int(h, 16))[2:].zfill(hash_length)
        binary_target = hash_binary[:difficulty]

        # Generate random token and save it in the database
        token = str(uuid4())
        # Prefix can add some precoditions to the cracking process
        # If we know we've tried all 2-length-long password set 
        prefix = 'aBBB'
        self.db.set_new_task(token, hashtype, binary_target, prefix, hashId)

        return_data = {
            "target": binary_target,
            "hash_type": hashtype,
            "token": token,
            "prefix": prefix
        }
        return return_data
    

    def verify_task(self, data):
        db_token, db_used, db_hashtype, db_target, db_prefix, hashId = self.db.get_task(data['token'])[0]
        # Return false if token already used
        if db_used == True:
            return False
        
        value_hashed = self.hash(data["value"].encode("utf-8"), db_hashtype)
        hash_length = self.get_hashtype_info(db_hashtype) 
        value_hashed_binary = self.hex_to_binary(value_hashed, hash_length)
        value_hashed_binary_trimmed = value_hashed_binary[:len(db_target)]

        if value_hashed_binary_trimmed == db_target and data['value'].startswith(db_prefix):
            self.db.update_token(db_token, True)
            # If the target is met additionally check if it's cracked
            self.check_if_cracked(hashId, data["value"], db_hashtype)
            return True
        
        return False
    

    def check_if_cracked(self, hashId, value, db_hashtype):
        db_hash = self.db.get_hash(hashId)[0][1]
        value_hashed = self.hash(value.encode("utf-8"), db_hashtype)
        if value_hashed == db_hash:
            self.db.set_hash_as_cracked(hashId, True, value)



if __name__ == "__main__":
    worker = WorkDispatcher()
    worker.get_hashtype_info("MD5")