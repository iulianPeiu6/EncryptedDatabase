import sqlite3
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
            files.append(File(file[File.index["id"]],
                              file[File.index["name"]],
                              file[File.index["crypt_alg"]],
                              file[File.index["encrypt_key"]],
                              file[File.index["decrypt_key"]]))
        con.close()
        return files
    except Exception as e:
        print(e)


def add():
    try:
        con = sqlite3.connect('files.db')

        cur = con.cursor()
        cur.execute(r"INSERT INTO files(name, crypt_alg, encrypt_key, decrypt_key) VALUES ('test1.txt',"
                    r"'rsa',"
                    r"'encrypt_key',"
                    r"'decrypt_key')")
        con.commit()

        con.close()
    except Exception as e:
        print(e)