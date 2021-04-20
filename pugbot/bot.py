"""
This bot requires:
    read message permission
    write message permission
    move members permission
    view channel permission
    create channel permission
    delete channel permission
"""
import logging
import sys
import json

import discord
from discord.ext import commands

from pugbot import conf, loggers


# logger
logger = logging.getLogger('pugbot.bot')


class PugBot(commands.Bot):
    """
    The PugBot definition.
    """

    async def on_ready(self):
        """
        When the bot is ready, this function is called.
        """
        logger.info("Bot is ready!")
        logger.info(
            f"These commands were loaded: "
            f"{json.dumps(self.all_commands, indent=4, default=str)}",
        )
        loggers  # VOID call to initialize the loggers

        # if conf.TEST_MODE:
        #     logger.info("Bot is running tests now!")
        #     # If TEST_MODE is enabled, run all the tests
        #     import nose
        #     import nest_asyncio
        #     nest_asyncio.apply()
        #     nose.main()
        #     sys.exit()

    async def on_message(self, message: discord.Message):
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
            debug_string = "Message received!\n"
            if message.guild:
                debug_string += f"--> Guild: {message.guild}({message.guild.id})\n"
                debug_string += f"--> Channel: #{message.channel}({message.channel.id})\n"
                debug_string += f"--> Author: @{message.author}({message.author.id}): "
            else:
                debug_string += f"--> Channel: #{message.channel}({message.channel.id}): "
            debug_string += f"{message.content}\n"
            debug_string += f"--> Jump URL: [{message.jump_url}]\n"
            logger.info(debug_string)

        await super().on_message(message)
    
    async def invoke(self, ctx):
        """
        When the bot is attempting to invoke a command
        """
        await super().invoke(ctx)

    async def send_message(self, message, channel: discord.TextChannel):
        """
        Sends a message to a channel when the bot is initialized
        """
        return channel.send(message)


# Initialize the bot
bot = PugBot(command_prefix=conf.PREFIX)