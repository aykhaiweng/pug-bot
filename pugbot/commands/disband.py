"""
Create a Pug
"""
from discord.ext.commands import command

from .. import conf
from ..exceptions import PugNotFound
from ..pugs import PugListHandler


@command()
async def disband(ctx, *args):
    f"""
    If you are the lobby owner, this disbands the pug

    Checks: 

    Syntax: {conf.PREFIX}
    """

    # Get the pug by the lobby
    try:
        pug = PugListHandler.get_pug_by_channel(ctx.guild.id, ctx.channel)
    except PugNotFound:
        # If no pugs could be found, send an error message and exit the function
        await ctx.send(f"There are no on-going pugs in {ctx.channel}. Use `{conf.PREFIX}create` to create one.")
        return

    # if pug.owner == ctx.author:
    PugListHandler.remove_pug(pug)  # We'll just let anyone do it now

    # Send an embed for the new pug
    await ctx.send("The pug has been disbanded.")