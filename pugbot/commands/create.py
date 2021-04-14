"""
Create a Pug
"""
from discord.ext.commands import command

from ..utils import create_embed
from ..pugs import Pug, add_to_pug_list


@command()
async def create(ctx, *args):
    """
    Used for testing
    """
    if not args:
        await ctx.send(f"ERROR: {ctx.command} requires <name> <size> arguments")
        return
    
    # Turn that pesky tuple into a list so that we can pop it out later
    args = list(args)

    # default size
    size = 10
    # Attempt to get size
    if len(args) > 1:
        # This is to avoid `$create 10` from confusing the bot
        size = args[-1]
        try:
            size = int(args[-1])
            args.pop(-1)
        except ValueError:  # ValueError pops up when int fails
            pass

    # Now the name
    name = " ".join(args)

    # Create the new pug
    new_pug = Pug(
        name=name,
        owner=ctx.author,
        guild=ctx.guild,
        max_size=size,
    )

    # Add the pug to the list of available pugs
    add_to_pug_list(new_pug)

    # Send an embed for the new pug
    await ctx.send(embed=await create_embed(new_pug))
    
