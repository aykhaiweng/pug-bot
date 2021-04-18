from pugbot import conf
from pugbot.bot import bot
from pugbot.exceptions import PugNotFound
from pugbot.pugs import PugListHandler, create_pug_embed


@bot.command()
async def join(ctx, *args):
    """
    Adds a you to the Pug in this text-channel.
    """

    # Get the pug by the lobby
    try:
        pug = PugListHandler.get_pug_by_channel(ctx.guild, ctx.channel)
    except PugNotFound:
        await ctx.send(f"There are no on-going pugs in {ctx.channel}. Use `{conf.PREFIX}create` to create one.")
        return

    # Fail silently if the author is already part of the players
    if ctx.author in pug.players:
        return

    # Check that the players currently in the pug is not equal to or more than the max_size
    if len(pug.players) >= pug.max_size:
        # If the pug is full, call this person names
        await ctx.send(embed=await create_pug_embed(pug, footer=f"It's already full, dingus!"))
        return

    # Add the player to the pug
    pug.add_player(ctx.author)

    # Send an embed for the new pug
    await ctx.send(embed=await create_pug_embed(pug, footer=f"{ctx.author.name} has joined the party!"))

