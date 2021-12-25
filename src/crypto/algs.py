import rsa
from enum import Enum
from rsa import PublicKey, PrivateKey


class Settings(int, Enum):
    DEFAULT_KEY_SIZE = 256


class RSA(object):
    @staticmethod
    def generate_keys():
        return rsa.newkeys(Settings.DEFAULT_KEY_SIZE)

    @staticmethod
    def encrypt(msg, key: PublicKey):
        return rsa.encrypt(str.encode(msg), key)

    @staticmethod
    def decrypt(msg_bytes, key: PrivateKey):
        return rsa.decrypt(msg_bytes, key).decode()

