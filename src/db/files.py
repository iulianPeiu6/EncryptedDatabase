import os
import sqlite3
import shutil
from os import path


class File(object):

    def __init__(self, id, name, crypt_alg, encrypt_key, decrypt_key):
        self.id = id
        self.name = name
        self.crypt_alg = crypt_alg
        self.encrypt_key = encrypt_key
        self.decrypt_key = decrypt_key

    def __str__(self):
        return f"({self.id}, '{self.name}', '{self.crypt_alg}', '{self.encrypt_key}', '{self.decrypt_key}')"

    index = {
        "id": 0,
        "name": 1,
        "crypt_alg": 2,
        "encrypt_key": 3,
        "decrypt_key": 4
    }

    default_db_files_directory = path.join("..", "data")


def init_db():
    try:
        con = sqlite3.connect('files.db')
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS files")
        cur.execute('''
            CREATE TABLE files (
                id integer primary key, 
                name text not null, 
                crypt_alg text not null, 
                encrypt_key text, 
                decrypt_key text)''')
        con.commit()
        con.close()
    except Exception as e:
        print(e)


def get_all():
    try:
        con = sqlite3.connect('files.db')
        cur = con.cursor()
        sql_response = cur.execute('SELECT * FROM files')
        files = []
        for file in sql_response:
            id = file[File.index["id"]]
            name = file[File.index["name"]]
            crypt_alg = file[File.index["crypt_alg"]]
            encrypt_key = file[File.index["encrypt_key"]]
            decrypt_key = file[File.index["decrypt_key"]]
            mapped_file = File(id, name,crypt_alg, encrypt_key, decrypt_key)
            files.append(mapped_file)
        con.close()
        return files
    except Exception as e:
        print(f"ERROR \tCould not list files from database. Error message: '{e}'")


def add(file_metadata: File, filepath: str) -> bool:
    try:
        print(f"DEBUG \tCopy file {filepath} in db files directory: {File.default_db_files_directory}")
        shutil.copy(filepath, File.default_db_files_directory)
        con = sqlite3.connect('files.db')

        cur = con.cursor()

        print(f"DEBUG \tAdd file in database: {file_metadata}")
        sql_cmd = f"INSERT INTO files(name, crypt_alg, encrypt_key, decrypt_key) VALUES (" \
                       f"'{file_metadata.name}'," \
                       f"'{file_metadata.crypt_alg}'," \
                       f"'{file_metadata.encrypt_key}'," \
                       f"'{file_metadata.decrypt_key}') "
        print(f"DEBUG \tExecuting sql command: '{sql_cmd}'")

        cur.execute(sql_cmd)
        con.commit()

        con.close()
        return True
    except Exception as e:
        print(f"ERROR \tCould not add file to database. Error message: '{e}'")
        return False


def remove(name: str) -> bool:
    try:
        os.remove(os.path.join(File.default_db_files_directory, name))
        con = sqlite3.connect('files.db')
        sql_cmd = f"DELETE FROM files WHERE name='{name}'"
        print(f"DEBUG \tExecuting sql command: '{sql_cmd}'")
        cur = con.cursor()
        cur.execute(sql_cmd)
        con.commit()
        return True
    except Exception as e:
        print(f"ERROR \tCould not remove file to database. Error message: '{e}'")
        return False


def read(name: str) -> None:
    try:
        file = open(os.path.join(File.default_db_files_directory, name))
        content = file.read()
        print(f"INFO \tFile content: \n\r{content}")
    except Exception as e:
        print(f"ERROR \tCould not read file from database. Error message: '{e}'")
