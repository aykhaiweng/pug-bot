"""
Create a Pug
"""
from discord.ext.commands import command

from .. import conf
from ..exceptions import PugNotFound
from ..pugs import PugListHandler, create_pug_embed


@command()
async def status(ctx, *args):
    f"""
    Grabs the status of a PUG

    Checks: if ctx.user is owner of a pug => FAIL
            if ctx.channel already has a pug => FAIL
            if ctx.channel has no voice channels in the same category => FAIL
            if no <name> given => FAIL

    Syntax: {conf.PREFIX}
    """
    # Check if there is a pug in this channel
    try:
        existing_pug = PugListHandler.get_pug_by_channel(ctx.guild.id, ctx.channel)
        await ctx.send(embed=await create_pug_embed(existing_pug))
        # If there is an existing pug in this channel, send a friendly reminder
    except PugNotFound:
        await ctx.send(f"There are no on-going pugs in {ctx.channel}. Use `{conf.PREFIX}create` to create one.")
        return  # Do nothing