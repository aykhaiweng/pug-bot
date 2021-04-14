"""
Just a file full of constants, don't worry I'll document it.
"""
import os
from enum import Enum
import discord

# Prefix for the commands
PREFIX = os.getenv("PREFIX", "$")

class PugStatus(Enum):
    """
    Controlling the Pug statuses
    """
    OPEN = {'id': 0, 'color': discord.Color.green(), 'footer_message': "This PUG has stopped."}
    STARTED = {'id': 1, 'color': discord.Color.red(), 'footer_message': "This PUG has started."}
    ENDED = {'id': 2, 'color': discord.Color.blue(), 'footer_message': "This PUG has ended."}