"""
Created more for debugging purposes than anything else
"""
from pugbot.bot import bot


@bot.command()
async def hello(ctx):
    """
    Say hello to the bot! He might give you some interesting insights!
    """
    await ctx.send("Hi!")