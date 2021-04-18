from discord.ext import commands

from pugbot import conf, exceptions
from pugbot.pugs import PugListHandler, Pug


ERRORS = {
    'no_dm': "Hey, no DMs!",
    'only_one_pug_per_text_channel': (
        "There is already a pug in this channel: {existing_pug.name}. "
        "Type `{conf.PREFIX}join` to join the party!"
    ),
    'requires_pug_in_text_channel': 
        "There are no on-going pugs in {ctx.channel}. "
        "Use `{conf.PREFIX}create` to create one."

}


def guild_only():
    """
    Decorator for commands that only allow Guild messages. No DMs
    """
    async def predicate(ctx):
        if ctx.guild is None:
            raise exceptions.NoPrivateMessages(ERRORS['no_dm'])
        return True
    return commands.check(predicate)


def only_one_pug_per_text_channel():
    """
    Doesn't allow there to be more than one Pug per text-channel
    """
    async def predicate(ctx):
        existing_pug = PugListHandler.get_pug_by_channel(
            ctx.guild, ctx.channel
        )
        if existing_pug:
            raise exceptions.OnePugPerTextChannel(
                ERRORS['only_one_pug_per_text_channel'].format(
                    existing_pug=existing_pug,
                    conf=conf
                )
            )
        return True
    return commands.check(predicate)


def requires_pug_in_text_channel():
    """
    Only allow if there is a pug in the text-channel
    """
    async def predicate(ctx):
        existing_pug = PugListHandler.get_pug_by_channel(
            ctx.guild, ctx.channel
        )
        if not existing_pug:
            raise exceptions.OnePugPerTextChannel(
                f"There is already a pug in this channel: {existing_pug.name}. "
                f"Type `{conf.PREFIX}join` to join the party!"
            )
        return True
    return commands.check(predicate)