import db.files


def test_db_add_file():
    db.files.init_db()
    file = db.files.File(None, "test1", "rsa", "encrypt_key", "decrypt_key")
    db.files.add(file, r"D:\FII\Temp\test1.txt")
    files = db.files.get_all()
    print(files[0])


if __name__ == '__main__':
    test_db_add_file()
