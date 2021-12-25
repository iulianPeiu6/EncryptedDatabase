import re
from enum import Enum

from app.cmd_handler import EDCommandHandler


class Command(str, Enum):
    GET_ALL = r"^\s*ls" \
              r"\s*(-a|--all)\s*$"
    ADD = r"^\s*add" \
          r"\s*(-f|--file)\s*'(?P<filepath>[\/\\].*?\.[\w:]+)'" \
          r"(\s*(-alg|--algorithm)\s*(?P<algorithm>[\w]+))?" \
          r"(\s*(-n|--name)\s*(?P<name>[\w]+))?\s*$"


class EDCommandLine(object):
    def __init__(self):
        self.get_all_cmd = re.compile(Command.GET_ALL.value)
        self.add_cmd = re.compile(Command.ADD.value)

    def run(self):
        while True:
            command = input("Command:>\t")
            self.handle_command(command)

    def handle_command(self, command):
        if self.get_all_cmd.match(command):
            EDCommandHandler.handle_list_files_cmd()
        elif options := self.add_cmd.match(command):
            filepath = options.group("filepath")
            alg = options.group("algorithm")
            name = options.group("name")
            EDCommandHandler.handle_add_file_cmd(filepath, name, alg)
