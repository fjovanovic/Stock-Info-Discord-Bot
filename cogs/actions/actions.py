import datetime as dt
from math import ceil

from discord import app_commands
from discord import Interaction, Embed, Colour
from discord.app_commands import Transform
from discord.ext.commands import Cog, Bot

from constants import YAHOO_FINANCE_URL
from utils import utils
from components.my_errors import YfinanceMissingData
from components.my_transformers import TransformUpper
from .my_view_actions import MyViewActions


class Actions(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    
    @app_commands.command(name='actions', description='Stock actions (dividens, stock splits)')
    @app_commands.describe(
        ticker='Ticker symbol'
    )
    async def actions(
        self, 
        interaction: Interaction, 
        ticker: Transform[str, TransformUpper]
    ) -> None:
        await interaction.response.defer()

        data = utils.fetch_data(ticker)
        act = data.actions
        if act is None:
            raise YfinanceMissingData

        size = act.shape[0]
        dates = '\n'.join([dt.datetime.strftime(date, "%Y-%m-%d") for date in act.index][0:10])
        dividens = '\n'.join([f'{float(div):.2f}' for div in act['Dividends']][0:10])
        splits = '\n'.join([f'{float(spl):.2f}' for spl in act['Stock Splits']][0:10])

        my_view = MyViewActions(ticker, act, 0, size)

        my_embed = Embed(
            title='More info',
            url=f'{YAHOO_FINANCE_URL}{ticker}',
            colour=Colour.blue(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'{ticker} | Page 1 / {ceil(size / 10)}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(name='Date', value=f'```\n{dates}```', inline=True)
        my_embed.add_field(name='Dividens', value=f'```\n{dividens}```', inline=True)
        my_embed.add_field(name='Stock Splits', value=f'```\n{splits}```', inline=True)

        await interaction.followup.send(embed=my_embed, view=my_view)
    

    async def cog_load(self) -> None:
        print(f'Cog loaded: {self.__class__.__name__}')


async def setup(bot: Bot) -> None:
    await bot.add_cog(Actions(bot=bot))