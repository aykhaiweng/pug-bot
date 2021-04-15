"""
Just a file full of constants, don't worry I'll document it.
"""
from enum import Enum


# Enums
class PugStatus(Enum):
    """
    Controlling the Pug statuses
    """
    OPEN = 0
    STARTED = 1
    ENDED = 2