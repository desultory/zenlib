from logging import Logger
from typing import Protocol


class HasLogger(Protocol):
    logger: Logger
