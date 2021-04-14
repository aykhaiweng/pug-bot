import os
from pugbot.bot import bot

# Default token retrieved from: https://discord.com/developers/applications/831476145063985162/bot
bot.run(os.getenv('TOKEN'))