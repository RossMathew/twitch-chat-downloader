from typing import List
from app import Singleton
from datetime import datetime


class Logger(metaclass=Singleton):
    QUIET: int = 0
    INFO: int = 1
    VERBOSE: int = 2
    DEBUG: int = 3

    def __init__(self, level: int, save: bool = False, output: str = 'output.log'):
        self.level: int = level
        self.save: bool = save
        self.output: str = output
        self.entries: List[str] = []

    def log(self, message: str):
        self.entries.append(message)
        print(message)
