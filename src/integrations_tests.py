import db.files
from logging.logger import defaultLogger as log


def test_db_files():
    db.files.init_db()
    file = db.files.File(None, "test1.txt", "rsa", "encrypt_key", "decrypt_key")
    db.files.add(file, r"D:\FII\Temp\test1.txt")
    files = db.files.get_all()

    for file in files:
        log.debug(file)
        db.files.read(file.name)

    db.files.remove("test1.txt")
    files = db.files.get_all()

    for file in files:
        log.debug(file)


if __name__ == '__main__':
    test_db_files()
