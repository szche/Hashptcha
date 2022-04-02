import binascii
import hashlib
from queue import Empty
import string
from itertools import product
from math import ceil 

HASH = 'a3dcb4d229de6fde0db5686dee47145d'

# Diff is the % of hashes that can be accepted
# 00000...0000 - ffffff......ffff
# with diff = 1 only 1% of hashes get accepted

class Targeter():
    def __init__(self):
        self.dictionary = string.ascii_letters + string.digits


    def bump_prefix(self, prefix):
        #print("Got old prefix: ", prefix)
        if prefix == '':
            prefix_binary = '0'*8
        else: 
            prefix_binary = prefix
        #print(prefix_binary)
        prefix_binary_incremented = self.increment_binary(prefix_binary)
        prefix_binary_incremented = prefix_binary_incremented.zfill(8* ceil(len(prefix_binary_incremented)/8) )
        #print(prefix_binary_incremented, len(prefix_binary_incremented))
        print("New prefix: ", prefix_binary_incremented, len(prefix_binary_incremented))
        b = int(prefix_binary_incremented, 2).to_bytes(len(prefix_binary_incremented) // 8, byteorder='big')
        print(b)
        return prefix_binary_incremented
        n = int(prefix_binary_incremented, 2)
        new_prefix = binascii.unhexlify('%x' %n).decode('utf-8')
        print(new_prefix)
        return new_prefix

    def increment_binary(self, b):
        return '{:08b}'.format(1 + int(b, 2))

class Miner():
    def __init__(self):
        self.dictionary = string.ascii_letters + string.digits

    def hash_md5(self, data):
        return hashlib.md5(data).hexdigest()

    def hex_to_binary(self, data):
        return bin(int(data, 16))[2:].zfill(128)

    def mine(self, hash, target_lower, target_upper, prefix):
        print("Mining new task...")
        leng = 1
        work = True
        hash_counter = 0
        while work:
            for p in (''.join(i) for i in product(self.dictionary, repeat = leng)):
                text = prefix + p
                hash = self.hash_md5(text.encode('utf-8'))
                hash_counter += 1
                hash_int = int(hash, 16)
                if hash_int >= target_lower and hash_int <= target_upper:
                    print("Found: ", text)
                    print("P: ", p)
                    print(hash_int)
                    print(hash_counter)
                    work = False
                    break
            leng+=1
            
        return hash_counter
        







def calculate_target(diff, h):
    hash_min = 0
    hash_max = 'f' * len(h)
    hash_max_int = int(hash_max, 16)
    p = int(int(hash_max, 16) * (diff/100))
    hash_int = int(h, 16)
    print("Hashes accepted: ", p)
    print("Hash as int: ", hash_int)
    print("Max hash int: ", hash_max_int)
    print("-" * 20)
    upper_limit = hash_int + p
    if upper_limit > hash_max_int:
        upper_limit = hash_max_int
    
    lower_limit = hash_int - p
    if lower_limit < 0:
        lower_limit = 0
    print("Upper limit: ", upper_limit )
    print("Lower limit: ", lower_limit )
    return lower_limit, upper_limit





if __name__ == "__main__":
    # lower, upper = calculate_target(0.0001, HASH)
    # miner = Miner()
    # miner.mine(HASH, lower, upper, 'aaa')
    t = Targeter()
    prefix = ''
    for i in range(1000):
        prefix = t.bump_prefix(prefix)
