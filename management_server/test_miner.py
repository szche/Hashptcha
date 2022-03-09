import hashlib
import string
from itertools import product


class Miner():
    def __init__(self):
        self.dictionary = string.ascii_letters + string.digits

    def hash_md5(self, data):
        return hashlib.md5(data).hexdigest()

    def hex_to_binary(self, data):
        return bin(int(data, 16))[2:].zfill(128)

    def mine(self, task):
        #print("Mining new task...")
        data = {
            "token": task["token"],
            "value": None,
        }
        leng = 1
        work = True
        hash_counter = 0
        while work:
            for p in (''.join(i) for i in product(self.dictionary, repeat = leng)):
                text = task['prefix'] + p
                hash = self.hash_md5(text.encode('utf-8'))
                hash_counter += 1
                hash_binary = self.hex_to_binary(hash)
                if hash_binary.startswith( task['target'] ):
                    data["value"] = text
                    work = False
                    break
            leng+=1
            
        #print("Hash counter: ", hash_counter)
        #print(data)
        return data, hash_counter

    def benchmark_MD5(self, difficulty):
        sample_data = {"hash_type": 'MD5', "prefix": '', "target": '1', "token": '78044f12-7b67-42a7-a4da-b0c2c9cb251f'}
        hash_sum = 0
        cases = 0
        for p in (''.join(i) for i in product(self.dictionary, repeat = 2)):
            sample_data['prefix'] = p
            target = '0' * difficulty
            sample_data["target"] = target
            data, counter = self.mine(sample_data)
            cases += 1
            hash_sum += counter
        print("Total hashes: ", hash_sum)
        print("Tries: ", cases)
        print("Hases avg: ", hash_sum/cases)
        print("Difficulty: ", difficulty)
        print("-" * 50)
        



if __name__ == "__main__":
    miner = Miner()
    for i in range(15):
        miner.benchmark_MD5(i)
