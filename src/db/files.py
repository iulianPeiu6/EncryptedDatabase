"""DB files query and DMLs commands implementations
"""
import os
import sqlite3
from enum import Enum
from rsa import PrivateKey
from crypto.algs import RSA
from os import path
from ed_logging.logger import defaultLogger as log


class Settings(str, Enum):
    default_db_files_directory = path.join("..", "data")
    db_location = path.join("..", "data", ".db", "ED.db")


class File(object):
    """A model class representing a record in the files database
    """

    def __init__(self, id, name, crypt_alg, encrypt_key, decrypt_key):
        """File Constructor

        :param id: file id
        :param name: file name
        :param crypt_alg: file encryption algorithm that is used
        :param encrypt_key: file encryption key
        :param decrypt_key: file decryption key
        """

        self.id = id
        self.name = name
        self.crypt_alg = crypt_alg
        self.encrypt_key = encrypt_key
        self.decrypt_key = decrypt_key

    def __str__(self):
        """

        :return: a string representing the object
        """
        return f"({self.id}, '{self.name}', '{self.crypt_alg}', '{self.encrypt_key}', '{self.decrypt_key}')"

    index = {
        "id": 0,
        "name": 1,
        "crypt_alg": 2,
        "encrypt_key": 3,
        "decrypt_key": 4
    }


def init_db():
    """Initialize database.
    Create an empty database.
    Create an empty files table.
    """
    try:
        log.debug("Start initializing database")
        with sqlite3.connect(Settings.db_location.value) as con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS files")
            cur.execute('''
                CREATE TABLE files (
                    id integer primary key, 
                    name text not null UNIQUE, 
                    crypt_alg text not null, 
                    encrypt_key text, 
                    decrypt_key text)''')
            con.commit()
            con.close()
        log.debug("Database initialized")
    except Exception as e:
        log.error("Error while initializing database", e)


def get_all() -> list[File]:
    """List all files from database and map them to File object.

    :return: a list of files
    """
    try:
        with sqlite3.connect(Settings.db_location.value) as con:
            cur = con.cursor()
            sql_response = cur.execute('SELECT * FROM files')
            files = []
            for file in sql_response:
                id = file[File.index["id"]]
                name = file[File.index["name"]]
                crypt_alg = file[File.index["crypt_alg"]]
                encrypt_key = file[File.index["encrypt_key"]]
                decrypt_key = file[File.index["decrypt_key"]]
                mapped_file = File(id, name, crypt_alg, encrypt_key, decrypt_key)
                files.append(mapped_file)
        return files
    except Exception as e:
        log.error("Could not list files from database", e)


def add(file_metadata: File, filepath: str) -> bool:
    """Add a given file in database.

    :param file_metadata: file metadata:  name, encryption algorithm, keys
    :param filepath: local file path
    :return: True if success, False otherwise
    """

    try:
        log.debug(f"Creating file {filepath} in db files directory: {Settings.default_db_files_directory.value}")

        with open(filepath, "rb") as file:
            content = file.read()

        keys = RSA.generate_keys()
        file_metadata.encrypt_key = keys[0]
        file_metadata.decrypt_key = keys[1]

        with open(path.join(Settings.default_db_files_directory.value, file_metadata.name), "wb+") as  encrypted_file:
            encrypted_content = RSA.encrypt(content, file_metadata.encrypt_key)
            encrypted_file.write(encrypted_content)

        with sqlite3.connect(Settings.db_location.value) as con:
            cur = con.cursor()
            log.debug(f"Add file in database: {file_metadata}")
            sql_cmd = f"INSERT INTO files(name, crypt_alg, encrypt_key, decrypt_key) VALUES (" \
                      f"'{file_metadata.name}'," \
                      f"'{file_metadata.crypt_alg}'," \
                      f"'{file_metadata.encrypt_key}'," \
                      f"'{file_metadata.decrypt_key}') "
            log.debug(f"Executing sql command: '{sql_cmd}'")
            cur.execute(sql_cmd)
            con.commit()

        return True
    except Exception as e:
        log.error("Could not add file to database", e)
        return False


def remove(name: str) -> bool:
    """Delete a file from database

    :param name: the remote filename
    :return: True if success, False otherwise
    """

    try:
        os.remove(os.path.join(Settings.default_db_files_directory.value, name))
        con = sqlite3.connect(Settings.db_location.value)
        sql_cmd = f"DELETE FROM files WHERE name='{name}'"
        log.debug(f"Executing sql command: '{sql_cmd}'")
        cur = con.cursor()
        cur.execute(sql_cmd)
        con.commit()
        log.info("File removed")
        return True
    except Exception as e:
        log.error("Could not remove file to database", e)
        return False


def read(name: str):
    """Read a file from database

    Query file, decrypt file content and print it.

    :param name: remote file name
    """
    try:
        with sqlite3.connect(Settings.db_location.value) as con:
            log.debug(f"Get file metadata with name '{name}' from database")
            cur = con.cursor()
            sql_query = f"SELECT * FROM files WHERE name = '{name}'"
            log.debug(f"Executing sql query: '{sql_query}'")
            sql_response = cur.execute(sql_query)
            file_metadata = sql_response.fetchone()
            if file_metadata is None:
                raise Exception("File not found")
            file = File(file_metadata[File.index["id"]],
                        file_metadata[File.index["name"]],
                        file_metadata[File.index["crypt_alg"]],
                        file_metadata[File.index["encrypt_key"]],
                        file_metadata[File.index["decrypt_key"]])

        exec_local_vars = {}
        exec(f"decrypt_key={file.decrypt_key}", globals(), exec_local_vars)
        decrypt_key = exec_local_vars['decrypt_key']

        with open(os.path.join(Settings.default_db_files_directory.value, name), "rb") as file:
            content = file.read()
            decrypted_content = RSA.decrypt(content, decrypt_key)
            log.info(f"File content: \n\r{decrypted_content}")
    except Exception as e:
        log.error("Could not read file from database", e)
