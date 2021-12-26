"""Command analyser
"""
import re
from enum import Enum

from app.cmd_handler import EDCommandHandler


class Command(str, Enum):
    """Stores the regex representation of all available command
    """
    GET_ALL = r"^\s*ls" \
              r"\s*(-a|--all)\s*$"

    ADD = r"^\s*add" \
          r"\s*(-f|--file)\s*'(?P<filepath>[\/\\].*?\.[\w:]+)'" \
          r"(\s*(-alg|--algorithm)\s*(?P<algorithm>[\w]+))?" \
          r"(\s*(-n|--name)\s*(?P<name>[\w.]+))?\s*$"

    REMOVE = r"^\s*rm" \
             r"\s*(-f|--file)\s*(?P<name>[\w.]+)\s*$"

    READ = r"^\s*read" \
           r"\s*(-f|--file)\s*(?P<name>[\w.]+)\s*$"

    EXIT = r"^\s*(exit|quit|q)\s*$"


class EDCommandLine(object):
    def __init__(self):
        self.get_all_cmd = re.compile(Command.GET_ALL.value)
        self.add_cmd = re.compile(Command.ADD.value)
        self.remove_cmd = re.compile(Command.REMOVE.value)
        self.read_cmd = re.compile(Command.READ.value)
        self.exit_cmd = re.compile(Command.EXIT.value)

    def run(self):
        """Run the ED Application command line
        """
        while True:
            command = input("Command:>\t")
            self.handle_command(command)

    def handle_command(self, command):
        """Handle a given command

        :param command: the string representation of the command
        """
        if self.get_all_cmd.match(command):
            EDCommandHandler.handle_list_files_cmd()
        elif options := self.add_cmd.match(command):
            filepath = options.group("filepath")
            alg = options.group("algorithm")
            name = options.group("name")
            EDCommandHandler.handle_add_file_cmd(filepath, name, alg)
        elif options := self.remove_cmd.match(command):
            filename = options.group("name")
            EDCommandHandler.handle_remove_cmd(filename)
        elif options := self.read_cmd.match(command):
            filename = options.group("name")
            EDCommandHandler.handle_read_file_cmd(filename)
        elif self.exit_cmd.match(command):
            EDCommandHandler.handle_exit_cmd()
        else:
            EDCommandHandler.handle_unknown_cmd(command)