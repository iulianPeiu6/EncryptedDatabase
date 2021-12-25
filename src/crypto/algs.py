import rsa
from enum import Enum
from rsa import PublicKey, PrivateKey


class Alg(str, Enum):
    DEFAULT_ALG = "RSA"
    RSA = "RSA"


class Settings(int, Enum):
    DEFAULT_KEY_SIZE = 256


class RSA(object):
    @staticmethod
    def generate_keys():
        return rsa.newkeys(Settings.DEFAULT_KEY_SIZE)

    @staticmethod
    def encrypt(msg_bytes: bytes, key: PublicKey):
        return rsa.encrypt(msg_bytes, key)

    @staticmethod
    def decrypt(msg_bytes: bytes, key: PrivateKey):
        return rsa.decrypt(msg_bytes, key).decode()

