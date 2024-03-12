import datetime as dt

from discord import app_commands
from discord import Interaction, Embed, Colour
from discord.app_commands import Transform
from discord.ext.commands import Cog, Bot

from constants import YAHOO_FINANCE_URL
from utils import utils
from components.my_errors import YfinanceMissingData
from components.my_transformers import TransformUpper


class MajorHolders(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    
    @app_commands.command(name='major_holders', description='Major holders for the stock')
    @app_commands.describe(
        ticker='Ticker symbol'
    )
    async def major_holders(
        self, 
        interaction: Interaction, 
        ticker: Transform[str, TransformUpper]
    ) -> None:
        await interaction.response.defer()
        
        data = utils.fetch_data(ticker)
        holders = data.major_holders
        if holders is None:
            raise YfinanceMissingData

        my_embed = Embed(
            title='More info',
            url=f'{YAHOO_FINANCE_URL}{ticker}',
            colour=Colour.blue(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'{ticker}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(name='Shares Held by All Insider', value=f'`{holders.iloc[0][0]}`', inline=False)
        my_embed.add_field(name='Shares Held by Institutions', value=f'`{holders.iloc[1][0]}`', inline=False)
        my_embed.add_field(name='Float Held by Institutions', value=f'`{holders.iloc[2][0]}`', inline=False)
        my_embed.add_field(name='Number of Institutions Holding Shares', value=f'`{float(holders.iloc[3][0]):,}`', inline=False)

        await interaction.followup.send(embed=my_embed)
    

    async def cog_load(self) -> None:
        print(f'Cog loaded: {self.__class__.__name__}')


async def setup(bot: Bot) -> None:
    await bot.add_cog(MajorHolders(bot=bot))