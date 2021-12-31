"""Logger"""
from enum import Enum


class Environment(Enum):
    """Stores an enumeration of the possible environments: Production or Development."""
    DEVELOPMENT = 0
    PRODUCTION = 1


class Color:
    """Stores an enumeration of the colors used for logger customization."""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BASE = '\033[0m'


class LogLevel(str, Enum):
    """Stores an enumeration of the possible logging levels."""
    INFO = "INFO"
    DEBUG = "DEBUG"
    ERROR = "ERROR"


class Logger(object):
    """Logger model.
    The logging  is done differently regarding the environment where is running:
    Production or Development.

    In production the debug is disabled and the info and error tags are ignored
    and only the message is printed.
    """
    def __init__(self, env):
        """Constructor

        :param env: the environment where the application is running.
        """
        self._env = env

    def info(self, msg):
        """Log a message as a info.

        :param msg: the log message
        """
        if self._env == Environment.DEVELOPMENT:
            print(f"{Color.GREEN}{LogLevel.INFO}{Color.BASE} \t{msg}")
        else:
            print(msg)

    def debug(self, msg):
        """Log a message as a debug.

        :param msg: the log message
        """
        if self._env == Environment.DEVELOPMENT:
            print(f"{Color.BLUE}{LogLevel.DEBUG}{Color.BASE} \t{msg}")

    def error(self, msg, error):
        """Log a message as a error.

        :param msg: the log message
        :param error: the associated error
        """
        if self._env == Environment.DEVELOPMENT:
            print(f"{Color.RED}{LogLevel.ERROR}{Color.BASE} \t{msg}:'{error}'")
        else:
            print(f"{Color.RED}{msg}:'{error}'{Color.BASE}")


defaultLogger = Logger(Environment.DEVELOPMENT)
