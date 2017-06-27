from Cryptodome import Random
from Cryptodome.Cipher import AES
import hmac, hashlib


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

def generate_random(size: int):
    return Random.get_random_bytes(size)


def prf_hmac(key, message):
    digest_maker = hmac.new(key, message, hashlib.sha256)
    digest = digest_maker.hexdigest()
    return digest.encode('utf-8')


class AESCipher:
    def __init__(self, key):
        self.key = key
        self.block_size = 16

    def encrypt(self, plaintext):
        padded_plaintext = self._pad(plaintext)
        iv = ('\x00' * 16).encode('utf-8')
        assert len(padded_plaintext) % self.block_size == 0, print("PADDING FAILED")
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return cipher.encrypt(iv + bytes(padded_plaintext.encode('utf-8')))

    def decrypt(self, ciphertext):
        enc = ciphertext
        iv = '\x00' * 16
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[16:]))

    def _pad(self, s):
        return s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
