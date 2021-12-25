from enum import Enum

from app.cmd_handler import EDCommandHandler


class Command(str, Enum):
    GET_ALL = "ls -a"

class EDCommandLine(object):
    def __init__(self):
        pass

    def run(self):
        while True:
            command = input("Command:>\t")
            self.handle_command(command)

    def handle_command(self, command):
        if command == Command.GET_ALL:
            EDCommandHandler.handle_list_files_cmd()
