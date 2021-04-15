"""
Create a Pug
"""
from discord.ext.commands import command

from .. import conf
from ..exceptions import PugNotFound
from ..pugs import Pug, PugListHandler, create_pug_embed


@command()
async def create(ctx, *args):
    f"""
    Creates a Pug, assigning you as the leader and assigning you as the first player.

    Checks: if ctx.user is owner of a pug => FAIL
            if ctx.channel already has a pug => FAIL
            if ctx.channel has no voice channels in the same category => FAIL
            if no <name> given => FAIL

    Syntax: {conf.PREFIX}
    """
    # Check that the TextChannel's category has valid VoiceChannels
    if len(Pug.get_category_channels(ctx.channel)) < 1:
        await ctx.send(f"ERROR: {ctx.command} requires a category with at least one Voice Channel in it")
        return

    # Check that there are valid arguments
    if not args:
        await ctx.send(f"ERROR: {ctx.command} `<name> <size>`, numbskull.")
        return

    # Check if there is a pug in this channel
    try:
        existing_pug = PugListHandler.get_pug_by_channel(ctx.guild.id, ctx.channel)
        # If there is an existing pug in this channel, send a friendly reminder
        await ctx.send(f"There is already a pug in this channel: {existing_pug.name}. Type `{conf.PREFIX}join` to join the party!")
        return
    except PugNotFound:
        pass  # Do nothing)
    
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