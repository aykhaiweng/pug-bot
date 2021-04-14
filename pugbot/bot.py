import datetime

from discord.ext import commands

from .commands import (
    hello,
    create
)


# Define the bot


class PugBot(commands.Bot):

    async def on_ready(self):
        """
        When the bot is ready, output this message
        """
        print(f"Timestamp: {datetime.datetime.now().strftime('%c')}")
        print(f"Username: {bot.user.name}")
        print(f"ID: {bot.user.id}")

        """
        Tasks
        """
    
    async def invoke(self, ctx):
        """
        Just wanna see some debugs
        """
        print("========")
        print(f"User: {ctx.author}")
        print(f"Guild: {ctx.guild}")
        print(f"Command: {ctx.message.content}")
        print(f"Jump to message: {ctx.message.jump_url}")
        await super().invoke(ctx)


# Initialize the bot
bot = PugBot(command_prefix="$")


# Commands
bot.add_command(hello.hello)
bot.add_command(create.create)