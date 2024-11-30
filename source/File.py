from enum import Enum

class FileType(Enum):
    File = 1
    Archive = 2

class File:
    def __init__(self, type: FileType, name: str, content: str, neasted: list):
        self.type = type
        self.name = name
        self.content = content
        self.neasted = neasted