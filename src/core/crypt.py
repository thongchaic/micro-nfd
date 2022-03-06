from cryptolib import aes
from hashlib import sha1
import binascii
import ssl 

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
        return binascii.hexlify(self.sha1.digest())

    def hashCheck(self,hash1, data):
        hash2 = self.hash(data)
        return hash1 == hash2 

    def cert(self,_file):
        #nensec list -c 
        #  /ndn/th/ac/srru/tc
        #+->* /ndn/th/ac/srru/tc/KEY/%C6%B4P%98%10%E3%BB%E3
        #+->* /ndn/th/ac/srru/tc/KEY/%C6%B4P%98%10%E3%BB%E3/self/v=1638519330038
        #ndnsec cert-dump 
        #static
        C = """Bv0BQQc2CANuZG4IAnRoCAJhYwgEc3JydQgCdGMIA0tFWQgIxrRQmBDju+MIBHNl
                bGY2CAAAAX1/XNT2FAkYAQIZBAA27oAVWzBZMBMGByqGSM49AgEGCCqGSM49AwEH
                A0IABLS74LBdBfTRBtsjbEtAWbFmKFMS/iZfMMUGMqaR3A8dO/4LtEa7ZvCYkb/p
                MUJZRjKNyCQVw3AMWdDx9gKEt4gWVxsBAxwoByYIA25kbggCdGgIAmFjCARzcnJ1
                CAJ0YwgDS0VZCAjGtFCYEOO74/0A/Sb9AP4PMTk3MDAxMDFUMDAwMDAw/QD/DzIw
                NDExMTI4VDA4MTUzMBdGMEQCIFhkDE+yI/cWXLJTSediLe/QRoT1KI/rDn36YSv0
                8gWoAiAkUFnHJSUIR8Qc45k9lU5JoXevAih0npxBCd7LPbDn9w=="""
        return C 
        
    def sign(self, data):
        #private key in ~/.ndn/ndnsec-key-file/....privkey 
        pkey = """MHcCAQEEIPhEhxI51seE3GmUVu/UXbkl4WIlpo2elBhuhj2t6y4IoAoGCCqGSM49
                AwEHoUQDQgAEtLvgsF0F9NEG2yNsS0BZsWYoUxL+Jl8wxQYyppHcDx07/gu0Rrtm
                8JiRv+kxQllGMo3IJBXDcAxZ0PH2AoS3iA=="""
        