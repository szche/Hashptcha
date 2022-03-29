import random
import re
from database import Database
from uuid import uuid4
import hashlib
import string
from math import ceil

class WorkDispatcher:
    def __init__(self):
        self.db = Database()
        self.default_targets = {
            'SHA256': 18,
            'MD5': 20
        }

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

    def binary_to_bytes(self, binary):
        return int(binary, 2).to_bytes(len(binary) // 8, byteorder='big')

    def bump_binary_point(self, point):
        point_incremented = '{:08b}'.format(1 + int(point, 2))
        point_incremented_filled = point_incremented.zfill(8*ceil(len(point_incremented)/8))
        return point_incremented_filled

    def determine_start_point(self, previous_tasks):
        # If noone completed task with this hash before, start from '00000000' point
        if len(previous_tasks) == 0:
            return '0'*8
        # p[6] corelates with end points of previous tasks
        previous_end_points = [int(p[6], 2) for p in previous_tasks]
        # now find the highest end point and bump it by 1
        new_start_point = max(previous_end_points) + 1 
        new_start_point_binary = bin(new_start_point)[2::]
        new_start_point_binary = new_start_point_binary.zfill(8*ceil(len(new_start_point_binary)/8))
        return new_start_point_binary

    def select_task(self, hashes, key, difficulty=-1):
        # Skip all cracked hashes
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
        # Prefix adds some precoditions to the cracking process
        start_point = self.determine_start_point( self.db.find_tasks_for_hash(hashId) )

        # Determine website ID correlated with the pubkey
        website = self.db.get_website_by_pubkey(key)
        key = website[0][0]

        self.db.set_new_task(token, hashtype, binary_target, start_point, hashId, key)

        return_data = {
            "target": binary_target,
            "hash_type": hashtype,
            "token": token,
            "start_point": start_point
        }
        return return_data
    

    def verify_task(self, data):
        db_token, db_used, db_hashtype, db_target, db_start_point, hashId, suffix, db_website_id = self.db.get_task(data['token'])[0]
        # Return false if token already used
        if db_used == True:
            return False

        # Return false if website_id and data["secret_key"] not corelated
        website = self.db.get_website_by_privkey(data['secret_key'])
        if db_website_id != website[0][0]:
            return False


        solution_bytes = self.binary_to_bytes( data['value'] )
        soltion_hashed = self.hash( solution_bytes, db_hashtype )
        hash_length = self.get_hashtype_info(db_hashtype) 
        value_hashed_binary = self.hex_to_binary(soltion_hashed, hash_length)

        if value_hashed_binary.startswith(db_target) and int(data['value'], 2) >= int(db_start_point, 2):
            self.db.update_token(db_token, True, data['value'])
            self.check_if_cracked(hashId, data['value'], db_hashtype)
            return True

        return False
    

    def check_if_cracked(self, hashId, value, db_hashtype):
        db_hash = self.db.get_hash(hashId)[0][1]
        value_bytes = self.binary_to_bytes(value)
        value_hashed = self.hash(value_bytes, db_hashtype)
        if value_hashed == db_hash:
            self.db.set_hash_as_cracked(hashId, True, value)



if __name__ == "__main__":
    worker = WorkDispatcher()

