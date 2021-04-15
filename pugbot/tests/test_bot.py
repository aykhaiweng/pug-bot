import os
import unittest

from .. import conf
from ..bot import bot


class BotTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_bot_initialization(self):
        """
        Testing Discord Bot initialization with a valid token
        """
        response = await bot.send_message("$hello", conf.TEST_CHANNEL_ID)