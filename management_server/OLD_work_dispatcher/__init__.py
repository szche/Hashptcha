import random

class WorkDispatcher:
    def __init__(self):
        pass

    def get_hashtype_info(self, hashtype):
        if hashtype == "MD5":
            return 128
        elif hashtype == "SHA256":
            return 256

    def select_task(self, hashes, difficulty=6):
        hashId, h, hashtype, cracked, plaintext = random.choice(hashes)
        hash_length = self.get_hashtype_info(hashtype)        
        hash_binary = bin(int(h, 16))[2:].zfill(hash_length)
        binary_target = hash_binary[:difficulty]

        #TODO add random token associated with the captcha
        #TODO add some preconditions for calculating hashes
        #TODO for example it must start with "A"
        return_data = {
            "target": binary_target,
            "hash_type": hashtype,
            "token": "123"
        }
        print(return_data)
        return return_data
       

    def verify_task(self, data):
        pass


if __name__ == "__main__":
    worker = WorkDispatcher()
