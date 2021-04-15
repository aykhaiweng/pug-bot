import logging
import sys
import asyncio

from discord.ext import commands

from . import conf
from .loggers import log
from .commands import (
    hello,
    create,
    join,
    leave,
    disband,
    status,
    createteam
)


class PugBot(commands.Bot):
    """
    The PugBot definition.
    """

    async def on_ready(self):
        """
        When the bot is ready, this function is called.
        """
        log("Bot is ready!")

        if conf.TEST_MODE:
            log("Bot is running tests now!")
            # If TEST_MODE is enabled, run all the tests
            import nose
            import nest_asyncio
            nest_asyncio.apply()
            nose.main()
            sys.exit()

    async def on_message(self, message):
        """
        Adding an override to skip this function of the bot
        receives a message that is not part of the prefix command
        """
        if conf.TEST_MODE is False:
            if (
                message.author == self.user or
                message.content.startswith(conf.PREFIX) is False
            ):
                return

        if conf.DEBUG:
            log(
                f"{message.guild}({message.guild.id}) #{message.channel}({message.channel.id}) @{message.author}({message.author.id}): "
                f"{message.content} [{message.jump_url}]"
            )

        await super().on_message(message)
    
    async def invoke(self, ctx):
        """
        When the bot is attempting to invoke a command
        """
        await super().invoke(ctx)

    async def send_message(self, message_content, channel_id):
        """
        Send a message to a channel
        """
        channel = self.get_channel(int(channel_id))
        log(f"Bot is sending message `{message_content}` to channel `{channel}({channel_id})`")
        await channel.send(message_content)


# Initialize the bot
bot = PugBot(command_prefix=conf.PREFIX)


# Commands
bot.add_command(hello.hello)
bot.add_command(create.create)
bot.add_command(join.join)
bot.add_command(leave.leave)
bot.add_command(disband.disband)
bot.add_command(status.status)
bot.add_command(createteam.createteam)