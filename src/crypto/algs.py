"""Cryptography algorithms"""
import os
import random
import string

import pyaes as pyaes
import rsa
from enum import Enum
from rsa import PublicKey, PrivateKey


class Alg(str, Enum):
    """An enumeration of available encryption algorithms"""
    DEFAULT_ALG = "RSA"
    RSA = "RSA"
    AES_ECB = "AES_ECB"


class Settings(int, Enum):
    """Contains settings regarding: rsa default key size(bits), aes default key size(chars)"""
    RSA_DEFAULT_KEY_SIZE = 2048
    AES_DEFAULT_KEY_SIZE = 32


class RSA(object):
    """RSA algorithm: key generation, encryption and decryption"""
    @staticmethod
    def generate_keys() -> tuple[PublicKey, PrivateKey]:
        """Generate a tuple representing the public and private keys with the
        default size specified in the :py:class:`Settings`

        :returns: a tuple (:py:class:`rsa.PublicKey`, :py:class:`rsa.PrivateKey`)
        """
        return rsa.newkeys(Settings.RSA_DEFAULT_KEY_SIZE)

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


class AESKey(object):
    def __init__(self, key: str, iv: str):
        """Constructor

        :param key: key
        :param iv: initialization vector
        """
        self.key = key
        self.iv = iv

    def __repr__(self):
        return f"AESKey(\"{self.key}\", \"{self.iv}\")"

    def __str__(self):
        return f"AESKey(\"{self.key}\", \"{self.iv}\")"


class AES(object):
    """AES algorithm: key generation, encryption and decryption"""
    @staticmethod
    def generate_keys() -> tuple[AESKey, AESKey]:
        """Generate a tuple representing the public and private keys with the
        default size specified in the :py:class:`Settings`

        :returns: a tuple (:py:class:`AESKey`, :py:class:`AESKey`)
        """
        key = "".join(random.choices(string.ascii_letters + string.digits, k=Settings.AES_DEFAULT_KEY_SIZE.value))
        iv = "".join(random.choices(string.ascii_letters + string.digits, k=Settings.AES_DEFAULT_KEY_SIZE.value))
        return AESKey(key, iv), AESKey(key, iv)

    @staticmethod
    def ecb_encrypt(plaintext: str, aes_key: AESKey, block_size: int = 16) -> bytes:
        """Encrypt a text using a given key.

        :param plaintext: the text bytes that will be encrypted
        :param aes_key: the key used for encryption
        :param block_size: block size (in number of chars) (default 16)
        :return: the encrypted text bytes
        """
        key = aes_key.key
        plaintext = AES._add_padding(plaintext, block_size)

        blocks = [plaintext[i:i + block_size] for i in range(0, len(plaintext), block_size)]
        ciphertext = ""

        for block in blocks:
            cipher_block = AES._encrypt(block, key)
            ciphertext += cipher_block

        return ciphertext.encode()

    @staticmethod
    def ecb_decrypt(ciphertext: str, aes_key: AESKey, block_size: int = 16) -> str:
        """Decrypt a cypher using a given key.

        :param ciphertext: the cypher text that will be decrypted
        :param aes_key: the key used for decryption
        :param block_size: block size (in number of chars) (default 16)
        :return: the decrypted text
        """
        key = aes_key.key
        cipher_blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
        plaintext = ""

        for cipher_block in cipher_blocks:
            block = AES._decrypt(cipher_block, key)
            plaintext += block

        return plaintext.rstrip()

    @staticmethod
    def _encrypt(plaintext: str, key: str) -> str:
        """Encrypt a text block.

        :param plaintext:
        :param key:
        :return: the ciphertext
        """
        plaintext_bytes = [ord(c) for c in plaintext]
        aes = pyaes.AES(key.encode())
        ciphertext = aes.encrypt(plaintext_bytes)
        return "".join(chr(i) for i in ciphertext)

    @staticmethod
    def _decrypt(ciphertext: str, key: str) -> str:
        """Decrypt a text block.

        :param ciphertext: cypher text
        :param key: key
        :return: decrypted text
        """
        ciphertext_bytes = [ord(c) for c in ciphertext]
        aes = pyaes.AES(key.encode())
        plaintext = aes.decrypt(ciphertext_bytes)
        return "".join(chr(i) for i in plaintext)

    @staticmethod
    def _add_padding(plaintext, block_size=16):
        """Adds padding to a text to obtain a block of size.

        :param plaintext: text to pad
        :param block_size: block size (default 16)
        :return: the padded text with length of the block size
        """
        padding = ""

        for space_remaining in range(len(plaintext) % block_size, (len(plaintext) // block_size + 1) * block_size):
            padding += " "

        plaintext += padding
        return plaintext
