from discord.ext.commands import CheckFailure


class NoPrivateMessages(CheckFailure):
    """
    No Private Messages!
    """


class OnePugPerTextChannel(CheckFailure):
    """
    Only one Pug per text-channel
    """


class PugNameAlreadyExists(CheckFailure):
    """
    Pug names need to be unique per Guild
    """


class RequiresPug(CheckFailure):
    """
    Could not find Pug in the current text-channel
    """


class PugNotFound(CheckFailure):
    """
    Could not find Pug in the current text-channel
    """