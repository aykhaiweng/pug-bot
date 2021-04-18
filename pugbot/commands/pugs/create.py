import logging

from discord.ext import commands

from pugbot import conf
from pugbot.bot import bot
from pugbot.checks import (
    guild_only,
    only_one_pug_per_text_channel,
    category_must_have_voice_channels
)
from pugbot.pugs import Pug, PugListHandler, create_pug_embed


logger = logging.getLogger('commands.create')


@bot.command()
@guild_only()
@only_one_pug_per_text_channel()
async def create(ctx, *args):
    """
    Creates a Pug in the text-channel that this command is typed in.
    """
    # Check that there are valid arguments
    if not args:
        await ctx.send(f"ERROR: {ctx.command} `<name> <size>`, numbskull.")
        return
    
    # Turn that pesky tuple into a list so that we can pop it out later
    args = list(args)

    # Handling the input for Size
    if len(args) > 1:
        # This is to avoid `{conf.PREFIX}.create 10` from confusing the bot
        size = args[-1]
        try:
            size = int(args[-1])
            args.pop(-1)
        except ValueError:  # ValueError pops up when int fails
            size = 10  # Fallback Size
    else:
        size = 10  # Fallback Size

    # Handle the rest of the input after the pop()
    name = " ".join(args)

    # Create the object to be pickled
    pug = Pug(
        name=name,
        owner=ctx.author,
        guild=ctx.guild,
        lobby_channel=ctx.channel,
        max_size=size,
        players=[ctx.author],
    )

    PugListHandler.add_pug(pug)

    # Send an embed for the new pug
    await ctx.send(embed=await create_pug_embed(pug))


@create.error
async def create_error(ctx, error):
    logger.error(error)
    if (
        isinstance(error, commands.CheckFailure) or
        issubclass(error, commands.CheckFailure)
    ):
        await ctx.send(error)
    