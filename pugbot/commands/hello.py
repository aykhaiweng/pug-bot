"""
Created more for debugging purposes than anything else
"""
from discord.ext.commands import command

from ..pugs import get_pugs_for_guild


@command()
async def hello(ctx):
    """
    Used for testing
    """
    list_of_pugs = get_pugs_for_guild(ctx.guild)
    if list_of_pugs:
        await ctx.send(f"Hello to you too! These are the current on-going PUGs: {list_of_pugs}")
    else:
        await ctx.send(f"Hello to you too! There are currently no on-going PUGs")