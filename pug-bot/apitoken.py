import os

try:
    from .secret import *
except:
    TOKEN = os.getenv('DISCORD_TOKEN')
