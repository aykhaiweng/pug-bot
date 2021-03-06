from pugbot import conf
from pugbot.bot import bot
from pugbot.pugs import PugListHandler, create_pug_embed


@bot.command()
async def leave(ctx, *args):
    """
    Leave the Pug in the current text-channel if you've joined it
    """

    # Get the pug by the lobby
    pug = PugListHandler.get_pug_by_channel(ctx.guild.id, ctx.channel)

    if ctx.author not in pug.players:
        return

    # Remove the player from the list
    pug.remove_player(ctx.author)

    # If the author was the owner, set someone else as the owner
    if pug.players:
        pug.set_owner(pug.players[0])
    
    # Send an embed for the new pug
    await ctx.send(embed=await create_pug_embed(pug, footer=f"{ctx.author.name} has left the party!"))