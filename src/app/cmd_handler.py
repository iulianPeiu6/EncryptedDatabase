"""Command handler"""
import os
import sys

import db.files
from crypto.algs import Alg
from db.files import File
from ed_logging.logger import defaultLogger as log


class EDCommandHandler(object):
    """Contains a collection of command handlers implemented as static class methods"""
    @staticmethod
    def handle_list_files_cmd():
        """Handle the list files command.

        Displays all files details from database. If the environment is production
        it will print only the id and name of the file, otherwise it will print all
        the file details on the screen for debugging purposes
        """
        log.debug("Handling list all files command")
        files = db.files.get_all()
        for file in files:
            log.info(f"{file.id}: {file.name}")
            log.debug(file)

    @staticmethod
    def handle_add_file_cmd(filepath: str, name: str = None, alg: str = None, overwrite: bool = False):
        """Handle the add file command with different arguments like filepath(required),
        name(optional) and algorithm(optional).

        It takes a local file as saves it on the database encrypted.

        :param filepath: the path to the local file
        :param name: the remote filename. If not specified, the default will be the local
        filename
        :param alg: the encryption algorithm. If not specified, the default will be RSA
        :param overwrite: overwrite
        """
        filepath = filepath[1:]
        log.debug(f"Handling add file command. Given arguments: file= '{filepath}', name= '{name}', alg='{alg}")
        filename = os.path.basename(filepath)
        size = os.path.getsize(filepath)

        if alg is None:
            alg = Alg.DEFAULT_ALG.value

        if alg not in [item for item in Alg]:
            log.error("Validation error", "Not a valid encrypting algorithm provided")
            return

        file = File(None,
                    filename if name is None else name,
                    Alg.DEFAULT_ALG if alg is None else alg,
                    size,
                    None)
        db.files.add(file, filepath, overwrite)

    @classmethod
    def handle_remove_cmd(cls, filename: str):
        """Handle the remove file command. Arguments filename(required).

        It takes a remote file saved on database and deletes it.

        :param filename: the remote filename
        """
        log.debug(f"Handling remove file command. Given arguments: file= '{filename}'")
        db.files.remove(filename)

    @classmethod
    def handle_read_file_cmd(cls, filename):
        """Handle the read file command. Arguments filename(required).

        It takes a remote file and  displays its decrypted content on the screen.

        :param filename: the remote filename
        """
        log.debug(f"Handling read file command. Given arguments: file= '{filename}'")
        db.files.read(filename)

    @classmethod
    def handle_unknown_cmd(cls, command: str):
        """Handle an unknown command.

        Displays an appropriate error on the screen.

        :param command: the string representation of the command
        """
        log.error(f"Unknown command", command)

    @classmethod
    def handle_exit_cmd(cls):
        """Handle the exit command.

        Close the command line(application).
        """
        sys.exit()
