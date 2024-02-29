import datetime as dt
import numpy as np

from discord import app_commands
from discord import Interaction, Embed, Colour
from discord.app_commands import Transform
from discord.ext.commands import Cog, Bot

from constants import YAHOO_FINANCE_URL
from utils import utils
from components.my_errors import YfinanceMissingData
from components.my_transformers import TransformUpper


class EarningsDates(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    
    @app_commands.command(name='earnings_dates', description='Future (4) and historic (8) earnings dates')
    @app_commands.describe(
        ticker='Ticker symbol'
    )
    async def earnings_dates(
        self, 
        interaction: Interaction, 
        ticker: Transform[str, TransformUpper]
    ) -> None:
        await interaction.response.defer()
        
        data = utils.fetch_data(ticker)
        earnings = data.earnings_dates
        if earnings is None:
            raise YfinanceMissingData

        earnings.replace(np.nan, '?', inplace=True)
        dates = '\n'.join([dt.datetime.strftime(date, "%Y-%m-%d") for date in earnings.index])
        eps_est_rep = '\n'.join([f'{eps_est} / {eps_rep}' for (eps_est, eps_rep) in zip(earnings['EPS Estimate'], earnings['Reported EPS'])])
        surpise = '\n'.join([f'{float(val):.2f} %' if val != '?' else '?' for val in earnings['Surprise(%)'].astype(str)])

        my_embed = Embed(
            title='More info',
            url=f'{YAHOO_FINANCE_URL}{ticker}',
            colour=Colour.blue(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'{ticker}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(name='Earnings Date', value=f'```\n{dates}```', inline=True)
        my_embed.add_field(name='EPS est / rep', value=f'```\n{eps_est_rep}```', inline=True)
        my_embed.add_field(name='Surprise', value=f'```\n{surpise}```', inline=True)

        await interaction.followup.send(embed=my_embed)
    

    async def cog_load(self) -> None:
        print(f'Cog loaded: {self.__class__.__name__}')


async def setup(bot: Bot) -> None:
    await bot.add_cog(EarningsDates(bot=bot))