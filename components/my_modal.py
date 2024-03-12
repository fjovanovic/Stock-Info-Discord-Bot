import logging

from discord import Interaction
from discord.ui import Modal
from discord import Client

from utils import errors


class MyModal(Modal):
    async def on_error(self, interaction: Interaction[Client], error: Exception) -> None:
        logging.exception(error)

        await errors.error_embed(
            interaction,
            '⛔Unexpected error',
            'An unexpected error has occured. Please contact the admin'
        )