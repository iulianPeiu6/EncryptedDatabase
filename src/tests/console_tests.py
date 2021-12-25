import db.files
from crypto.algs import RSA
from ed_logging.logger import defaultLogger as log


def test_db_files():
    db.files.init_db()
    file = db.files.File(None, "test1.txt", "RSA", None, None)
    db.files.add(file, r"D:\FII\Temp\test1.txt")
    files = db.files.get_all()

    for file in files:
        log.debug(file)
        db.files.read(file.name)

    db.files.remove("test1.txt")
    files = db.files.get_all()

    for file in files:
        log.debug(file)


def test_rsa():
    keys = RSA.generate_keys()
    log.debug(keys)
    text = "Ana has apples"
    log.debug(f"Encrypting text:'{text}'")
    cypher_bytes = RSA.encrypt(text.encode(), keys[0])
    log.debug(f"Encrypted text:{cypher_bytes}")
    decrypted_text = RSA.decrypt(cypher_bytes, keys[1])
    log.debug(f"Decrypted text:'{decrypted_text}'")


if __name__ == '__main__':
    #test_db_files()
    test_rsa()
