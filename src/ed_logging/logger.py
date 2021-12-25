from enum import Enum


class Environment(Enum):
    DEVELOPMENT = 0
    PRODUCTION = 1


class LogLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    ERROR = "ERROR"


class Logger(object):
    def __init__(self, env):
        self._env = env

    def info(self, msg):
        if self._env == Environment.DEVELOPMENT:
            print(f"{LogLevel.INFO} \t{msg}")
        else:
            print(msg)

    def debug(self, msg):
        if self._env == Environment.DEVELOPMENT:
            print(f"{LogLevel.DEBUG} \t{msg}")

    def error(self, msg, error):
        if self._env == Environment.DEVELOPMENT:
            print(f"{LogLevel.ERROR} \t{msg}:'{error}'")


defaultLogger = Logger(Environment.DEVELOPMENT)
