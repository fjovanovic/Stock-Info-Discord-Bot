from typing import Any
import logging

from discord.ui import View, Item
from discord import Interaction, Client

from utils import errors


class MyView(View):
    async def on_error(self, interaction: Interaction[Client], error: Exception, item: Item[Any]) -> None:
        logging.exception(error)

        await errors.error_embed(
            interaction,
            '⛔Unexpected error',
            'An unexpected error has occured. Please contact the admin'
        )