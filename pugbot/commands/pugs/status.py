from pugbot import conf
from pugbot.bot import bot
from pugbot.exceptions import PugNotFound
from pugbot.pugs import PugListHandler, create_pug_embed


from pugbot.checks import  


@bot.command()
async def status(ctx, *args):
    """
    Shows the status of the Pug in the current text-channel.
    """
    # Check if there is a pug in this channel
    try:
        existing_pug = PugListHandler.get_pug_by_channel(ctx.guild, ctx.channel)
        await ctx.send(embed=await create_pug_embed(existing_pug))
        # If there is an existing pug in this channel, send a friendly reminder
    except PugNotFound:
        await ctx.send(f"There are no on-going pugs in {ctx.channel}. Use `{conf.PREFIX}create` to create one.")
        return  # Do nothing