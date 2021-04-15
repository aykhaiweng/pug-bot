"""
Here's a default error list
"""

errors = {
    'BAD_INPUT': ""
}


class BadInput(Exception):
    """
    Used for bad input
    """


class PugNotFound(Exception):
    """
    Pug not found
    """


class PugNameAlreadyExists(Exception):
    """
    Pug Name already Exists
    """