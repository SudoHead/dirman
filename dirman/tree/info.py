"""
Convenience classes for dealing with directory and file properties.
"""
from datetime import datetime
from enum import Enum

SIZE_SUFFIXES = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def datetime_formatter(time):
    return time.strftime("%Y-%m-%d at %H:%M:%S")


def time_now():
    return datetime_formatter(datetime.now())


class FileType(Enum):
    text = 1
    image = 2
    video = 3
    audio = 4
    binary = 5
    unknown = 6


class DirInfo:
    """
    Represents the properties of a directory.
    """

    def __init__(
            self, 
            upload_time: str = time_now(), 
            last_accessed: str = time_now(), 
            size: int = None,
            ):
        self.upload_time = upload_time
        self.last_accessed = last_accessed
        self.size = size

    def update(self, size_bytes: int) -> None:
        self.last_accessed = time_now()
        self.size = size_bytes

    def humansize(self):
        """
        Return the number of bytes in a human readable format.

        source: https://stackoverflow.com/questions/14996453/python-libraries-to-calculate-human-readable-filesize-from-bytes
        """
        if self.size is None:
            return "?B"
        i = 0
        nbytes = self.size
        while nbytes >= 1024 and i < len(SIZE_SUFFIXES) - 1:
            nbytes /= 1024.
            i += 1
        f = f"{nbytes:.2f}".rstrip('0').rstrip('.')
        return '%s%s' % (f, SIZE_SUFFIXES[i])

    def __str__(self):
        return f"{self.upload_time} {self.last_accessed} {self.humansize()}"


class FileInfo(DirInfo):
    """
    Represents the properties of a file.
    """

    def __init__(
            self, 
            type: FileType = FileType.unknown, 
            ):
        super().__init__()
        self.type = type

    def __str__(self):
        return f"{self.last_accessed} {self.humansize()} {self.type}"
