from pugbot import conf
from pugbot.bot import bot
from pugbot.exceptions import PugNotFound
from pugbot.pugs import PugListHandler


@bot.command()
async def disband(ctx, *args):
    """
    Disbands the Pug in the current text-channel.
    """

    # Get the pug by the lobby
    try:
        pug = PugListHandler.get_pug_by_channel(ctx.guild.id, ctx.channel)
    except PugNotFound:
        # If no pugs could be found, send an error message and exit the function
        await ctx.send(f"There are no on-going pugs in {ctx.channel}. Use `{conf.PREFIX}create` to create one.")
        return

    if ctx.author in pug.players:
        # Only players can close a pug
        PugListHandler.remove_pug(pug)  # We'll just let anyone do it now

    # Send an embed for the new pug
    await ctx.send("The pug has been disbanded.")