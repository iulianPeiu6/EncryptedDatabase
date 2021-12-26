from enum import Enum


class Environment(Enum):
    DEVELOPMENT = 0
    PRODUCTION = 1


class Color:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BASE = '\033[0m'


class LogLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    ERROR = "ERROR"


class Logger(object):
    def __init__(self, env):
        self._env = env

    def info(self, msg):
        if self._env == Environment.DEVELOPMENT:
            print(f"{Color.GREEN}{LogLevel.INFO}{Color.BASE} \t{msg}")
        else:
            print(msg)

    def debug(self, msg):
        if self._env == Environment.DEVELOPMENT:
            print(f"{Color.BLUE}{LogLevel.DEBUG}{Color.BASE} \t{msg}")

    def error(self, msg, error):
        if self._env == Environment.DEVELOPMENT:
            print(f"{Color.RED}{LogLevel.ERROR}{Color.BASE} \t{msg}:'{error}'")
        else:
            print(f"{Color.RED}{msg}:'{error}'{Color.BASE}")


defaultLogger = Logger(Environment.DEVELOPMENT)
