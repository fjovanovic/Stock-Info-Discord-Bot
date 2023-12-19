import logging

from discord import Interaction
from discord.app_commands import CommandTree, AppCommandError, CommandInvokeError

from utils import errors
from .my_errors import *


class MyCommandTree(CommandTree):
    async def on_error(self, interaction: Interaction, error: AppCommandError) -> None:
        logging.exception(error)

        if isinstance(error, CommandInvokeError):
            error = error.original

        if isinstance(error, YfinanceHTTPError):
            logging.exception(error)
            await errors.error_embed(
                interaction,
                '⛔Ticker not found',
                'Please double check if ticker symbol exist'
            )
        else:
            await errors.error_embed(
                interaction,
                '⛔Unexpected error',
                'An unexpected error has occured. Please contact the admin'
            )