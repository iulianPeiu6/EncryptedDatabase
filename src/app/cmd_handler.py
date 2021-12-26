import os
import sys

import db.files
from crypto.algs import Alg
from db.files import File
from ed_logging.logger import defaultLogger as log


class EDCommandHandler(object):
    @staticmethod
    def handle_list_files_cmd():
        log.debug("Handling list all files command")
        files = db.files.get_all()
        for file in files:
            log.info(f"{file.id}: {file.name}")
            log.debug(file)

    @staticmethod
    def handle_add_file_cmd(filepath, name=None, alg=None, ):
        filepath = filepath[1:]
        log.debug(f"Handling add file command. Given arguments: file= '{filepath}', name= '{name}', alg='{alg}")
        filename = os.path.basename(filepath)

        if alg is None:
            alg = Alg.DEFAULT_ALG.value

        if alg not in [item for item in Alg]:
            log.error("Validation error", "Not a valid encrypting algorithm provided")
            return

        file = File(None,
                    filename if name is None else name,
                    Alg.DEFAULT_ALG if alg is None else alg,
                    None,
                    None)
        db.files.add(file, filepath)

    @classmethod
    def handle_remove_cmd(cls, filename):
        log.debug(f"Handling remove file command. Given arguments: file= '{filename}'")
        db.files.remove(filename)

    @classmethod
    def handle_read_file_cmd(cls, filename):
        log.debug(f"Handling read file command. Given arguments: file= '{filename}'")
        db.files.read(filename)

    @classmethod
    def handle_unknown_cmd(cls, command):
        log.error(f"Unknown command", command)

    @classmethod
    def handle_exit_cmd(cls):
        sys.exit()
