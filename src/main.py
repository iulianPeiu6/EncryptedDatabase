import db.files

if __name__ == '__main__':
    db.files.init_db()
    db.files.add()
    files = db.files.get_all()
    print(files[0])
