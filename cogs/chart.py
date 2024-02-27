import datetime as dt
from io import BytesIO
from plotly.graph_objects import Figure, Candlestick

from discord import app_commands
from discord.app_commands import Choice
from discord import Interaction, Embed, Colour, File
from discord.app_commands import Transform
from discord.ext.commands import Cog, Bot

from constants import YAHOO_FINANCE_URL, CHART_PERIODS, CHART_INTERVALS
from utils import utils
from components.my_transformers import TransformUpper


class Chart(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    
    @app_commands.command(name='chart', description='Chart for the stock and given period and interval')
    @app_commands.describe(
        ticker='Ticker symbol',
        period='Time period',
        interval='Time interval'
    )
    @app_commands.choices(period=[Choice(name=period, value=period) for period in CHART_PERIODS])
    @app_commands.choices(interval=[Choice(name=interval, value=interval) for interval in CHART_INTERVALS])
    async def chart(
        self, 
        interaction: Interaction, 
        ticker: Transform[str, TransformUpper],
        period: str,
        interval: str
    ) -> None:
        await interaction.response.defer()
        
        data = utils.fetch_data(ticker)
        hist = data.history(period=period, interval=interval)

        fig = Figure(
            data=[
                Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close']
                )
            ]
        )

        fig.update_layout(font_family='Courier', font_size=10, title_x=0.5, template='plotly_dark', xaxis_rangeslider_visible=False)

        my_embed = Embed(
            title='More info',
            url=f'{YAHOO_FINANCE_URL}{ticker}',
            colour=Colour.blue(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'{ticker}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(name='Time period', value=f'`{period}`', inline=True)
        my_embed.add_field(name='Time interval', value=f'`{interval}`', inline=True)

        with BytesIO() as image_binary:
            fig.write_image(image_binary, 'PNG')
            image_binary.seek(0)
            my_file = File(fp=image_binary, filename='image.png')
            my_embed.set_image(url='attachment://image.png')

            await interaction.followup.send(embed=my_embed, file=my_file)
    

    async def cog_load(self) -> None:
        print(f'Cog loaded: {self.__class__.__name__}')


async def setup(bot: Bot) -> None:
    await bot.add_cog(Chart(bot=bot))