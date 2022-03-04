from cryptolib import aes
from hashlib import sha1
import ubinascii

class Crypt:
    BLOCK_SIZE = 16
    def __init__(self, key):
        self.key = key
        self.sha1 = sha1()
    
    def update(self,key='16-bytes-aes-key'):
        if len(key) != 16: #Use 16-byte key 
            raise Exception('AES 64-bit key required!')
        if not isinstance(key,(bytes)):
            key = bytes(key,'ascci')
        return aes(key, 1) #ECB Mode 

    def encrypt(self,plaintext):
        crypt = self.update(self.key)
        pad = BLOCK_SIZE - len(plaintext) % BLOCK_SIZE
        plaintext = plaintext + " "*pad
        return crypt.encrypt(plaintext)

    def decrypt(self,cipher):
        crypt = self.update(self.key)
        return crypt.decrypt(cipher)

    def hash(self,data):
        self.sha1.update(data)
        return ubinascii.hexlify(self.sha1.digest())

    def hashCheck(self,hash1, data):
        hash2 = self.hash(data)
        return hash1 == hash2 

    def cert(self,_file):
        pass
        
    def sign(self):
        pass 
    
