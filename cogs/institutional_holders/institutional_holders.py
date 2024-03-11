import datetime as dt

from discord import app_commands
from discord import Interaction, Embed, Colour
from discord.app_commands import Transform
from discord.ext.commands import Cog, Bot

from constants import YAHOO_FINANCE_URL
from utils import utils
from components.my_transformers import TransformUpper
from .my_view_institutional_holders import MyViewInstitutionalHolders
from .my_select_institutional_holders import MySelectInstitutionalHolders


class InstitutionalHolders(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    
    @app_commands.command(name='institutional_holders', description='Institutional holders for the stock')
    @app_commands.describe(
        ticker='Ticker symbol'
    )
    async def institutional_holders(
        self, 
        interaction: Interaction, 
        ticker: Transform[str, TransformUpper]
    ) -> None:
        await interaction.response.defer()

        data = utils.fetch_data(ticker)
        institutional_holders = data.institutional_holders
        size = institutional_holders.shape[0]

        my_view = MyViewInstitutionalHolders(ticker, institutional_holders, 0, size)
        my_select = MySelectInstitutionalHolders(institutional_holders)
        for i in range(1, size + 1):
            my_select.add_option(
                label=f'{institutional_holders.iloc[i-1]["Holder"]}',
                value=f'{i-1}',
                description=f'{institutional_holders.iloc[i-1]["Value"]:,} $'
            )
        my_view.add_item(my_select)

        my_embed = Embed(
            title='More info',
            url=f'{YAHOO_FINANCE_URL}{ticker}',
            colour=Colour.blue(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'{ticker}', icon_url=interaction.user.avatar.url)
        for (key, holder) in institutional_holders['Holder'].items():
            my_embed.add_field(
                name=f'Institutional holder #{int(key) + 1}',
                value=f'`{holder} ({institutional_holders.iloc[key]["Value"]:,} $)`',
                inline=False
            )

        await interaction.followup.send(embed=my_embed, view=my_view)
    

    async def cog_load(self) -> None:
        print(f'Cog loaded: {self.__class__.__name__}')


async def setup(bot: Bot) -> None:
    await bot.add_cog(InstitutionalHolders(bot=bot))