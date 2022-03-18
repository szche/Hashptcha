import random
import re
from database import Database
from uuid import uuid4
import hashlib
import string

class WorkDispatcher:
    def __init__(self):
        self.db = Database()
        self.default_targets = {
            'SHA256': 15,
            'MD5': 20
        }
        self.dictionary = string.ascii_letters + string.digits

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


    def bump_prefix(self, prefix):
        new_prefix = ''
        to_add = 1
        for char in prefix[::-1]:
            char_pos = self.dictionary.find(char)
            new_char = (char_pos + to_add) % len(self.dictionary)
            if new_char < char_pos:
                to_add = 1
            else:
                to_add = 0
            new_prefix += self.dictionary[new_char]
        new_prefix = new_prefix[::-1]
        if to_add == 1:
            new_prefix = new_prefix + self.dictionary[0]
        return new_prefix

    def sortPrefix(self, e):
        # Max prefix is detemined as follows:
        # 1) The longest and one with the highest value
        # Z > a, 9 > z, aa > 9
        sum = 0
        exponent = 0
        for char in e[::-1]:
            sum += (self.dictionary.find(char)+1) * (10**exponent)
            exponent+=1
        return sum

    def determine_prefix(self, previous_tasks):
        # if noone completed task with this hash before, start from the start
        if len(previous_tasks) == 0:
            return ""
        print(previous_tasks)
        previous_prefixes = [p[4]+p[6] for p in previous_tasks]
        previous_prefixes.sort(key=self.sortPrefix, reverse=True)
        max_prefix = previous_prefixes[0]
        return self.bump_prefix(max_prefix)

    def select_task(self, hashes, difficulty=-1):
        uncracked_hashes = [h for h in hashes if h[3] == 0]
        hashId, h, hashtype, cracked, plaintext = random.choice(uncracked_hashes)
        hash_length = self.get_hashtype_info(hashtype)  
        hash_binary = bin(int(h, 16))[2:].zfill(hash_length)

        #If difficulty is -1 it means the server wants the default taraget value
        if difficulty == -1:
            difficulty = self.default_targets[hashtype]

        binary_target = hash_binary[:difficulty]

        # Generate random token and save it in the database
        token = str(uuid4())
        # Prefix can add some precoditions to the cracking process
        # If we know we've tried all 2-length-long password set 
        prefix = self.determine_prefix( self.db.find_tasks_for_hash(hashId) )
        #prefix = 'aBBB'
        self.db.set_new_task(token, hashtype, binary_target, prefix, hashId)

        return_data = {
            "target": binary_target,
            "hash_type": hashtype,
            "token": token,
            "prefix": prefix
        }
        return return_data
    

    def verify_task(self, data):
        db_token, db_used, db_hashtype, db_target, db_prefix, hashId, suffix = self.db.get_task(data['token'])[0]
        # Return false if token already used
        if db_used == True:
            return False
        
        value_hashed = self.hash(data["value"].encode("utf-8"), db_hashtype)
        hash_length = self.get_hashtype_info(db_hashtype) 
        value_hashed_binary = self.hex_to_binary(value_hashed, hash_length)
        value_hashed_binary_trimmed = value_hashed_binary[:len(db_target)]
        received_suffix = data['value'][len(db_prefix):]

        if value_hashed_binary_trimmed == db_target and data['value'].startswith(db_prefix):
            self.db.update_token(db_token, True, received_suffix)
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
    worker.bump_prefix('999')