import logging

from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from sys import stdout, stderr
from typing import List, TextIO


LOG_FMT: str = "%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s"
LOG_DATE_FMT: str = "%Y-%m-%d %H:%M:%S"
STDOUT_FILTERS: List[int] = [logging.INFO]
STDERR_FILTERS: List[int] = [logging.DEBUG,
                             logging.ERROR,
                             logging.CRITICAL]


class LoggerNameException(Exception):
    """Logger Name Exception"""
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(self.msg)


def add_stream(stream: TextIO, filters: List[int], log: logging.Logger) -> None:
    """Add a stdout or stderr stream handler
    :param stream (Union[stdout, stderr])
    :param filters (List[int]): logging levels to filter
    :param log (logging.Logger): logger to add handlers to"""
    h: logging.StreamHandler = logging.StreamHandler(stream)
    h.addFilter(lambda log: log.levelno in filters)

    if stream == stdout:
        h.setLevel(logging.INFO)
    elif stream == stderr:
        h.setLevel(logging.ERROR)

    log.addHandler(h)


def construct(log_path: Path, name: str, level: str = "INFO", silent: bool = False) -> logging.Logger:
    """Construct logging.
    :param log_path: full file path to log file.
    :param name: log name (use '__name__' when calling this function).
    :param level: log level value, default is 'INFO'."""
    if not log_path.parent.exists():  # Create parent log directory path if it doesn't exist
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Construct the logger instance
    log = logging.getLogger(name)
    log.setLevel(level.upper())
    formatter = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATE_FMT)
    fh = TimedRotatingFileHandler(log_path, when="midnight", backupCount=31)  # rotate at midnight, 31 days of backup
    fh.setFormatter(formatter)
    log.addHandler(fh)
    add_stream(stream=stderr, filters=STDERR_FILTERS, log=log)  # Errors always print to stderr even with silent mode

    # Add the stdout log stream if not silent
    if not silent:
        add_stream(stream=stdout, filters=STDOUT_FILTERS, log=log)

    return logging.getLogger(name)
