"""Cryptography algorithms
"""
import rsa
from enum import Enum
from rsa import PublicKey, PrivateKey


class Alg(str, Enum):
    """An enumeration of available encryption algorithms
    """

    DEFAULT_ALG = "RSA"
    RSA = "RSA"


class Settings(int, Enum):
    """Contains settings regarding: default key size(bits)
    """

    DEFAULT_KEY_SIZE = 512


class RSA(object):
    """RSA algorithm: key generation, encryption and decryption
    """

    @staticmethod
    def generate_keys() -> tuple[PublicKey, PrivateKey]:
        """Generate a tuple representing the public and private keys with the
        default size specified in the :py:class:`Settings`

        :returns: a tuple (:py:class:`rsa.PublicKey`, :py:class:`rsa.PrivateKey`)
        """

        return rsa.newkeys(Settings.DEFAULT_KEY_SIZE)

    @staticmethod
    def encrypt(msg_bytes: bytes, key: PublicKey) -> bytes:
        """Encrypt a text bytes using a given key.

        :param msg_bytes: the text bytes that will be encrypted
        :param key: the public key used for encryption
        :return: the  encrypted text bytes
        """

        return rsa.encrypt(msg_bytes, key)

    @staticmethod
    def decrypt(msg_bytes: bytes, key: PrivateKey) -> str:
        """Decrypt a cypher bytes using a given key.

        :param msg_bytes: the cypher text bytes that will be decrypted
        :param key: the  private key used for decryption
        :return: the decrypted text
        """

        return rsa.decrypt(msg_bytes, key).decode()

