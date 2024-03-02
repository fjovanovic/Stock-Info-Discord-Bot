import datetime as dt
from math import ceil

from discord import (
    ButtonStyle, 
    Interaction, 
    Embed, 
    Colour
)
from discord.ui import View, Button
from discord.ui import button

from constants import YAHOO_FINANCE_URL
from .my_modal_actions import MyModalActions


class MyViewActions(View):
    def __init__(self, ticker: str, data: dict, page: int, size: int) -> None:
        super().__init__()
        self.ticker = ticker
        self.data = data
        self.page = page
        self.size = size
    
    
    @button(label='🢘 Previous', style=ButtonStyle.primary, disabled=True)
    async def previous_button(self, interaction: Interaction, button: Button) -> None:
        self.page -= 1
        if self.page == 0:
            self.children[0].disabled = True
        
        if self.page < ceil(self.size / 10):
            self.children[1].disabled = False
        
        start = self.page * 10
        end = self.page * 10 + 10
        
        dates = '\n'.join([dt.datetime.strftime(date, "%Y-%m-%d") for date in self.data.index][start:end])
        dividens = '\n'.join([f'{float(div):.2f}' for div in self.data['Dividends']][start:end])
        splits = '\n'.join([f'{float(spl):.2f}' for spl in self.data['Stock Splits']][start:end])

        my_embed = Embed(
            title='More info',
            url=f'{YAHOO_FINANCE_URL}{self.ticker}',
            colour=Colour.blue(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'{self.ticker} | Page {self.page + 1} / {ceil(self.size / 10)}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(name='Date', value=f'```\n{dates}```', inline=True)
        my_embed.add_field(name='Dividens', value=f'```\n{dividens}```', inline=True)
        my_embed.add_field(name='Stock Splits', value=f'```\n{splits}```', inline=True)

        await interaction.response.edit_message(embed=my_embed, view=self)
    

    @button(label='Next 🢚', style=ButtonStyle.primary)
    async def next_button(self, interaction: Interaction, button: Button) -> None:
        self.page += 1
        if self.page == 1:
            self.children[0].disabled = False
        
        if self.page + 1 >= ceil(self.size / 10):
            self.children[1].disabled = True

        start = self.page * 10
        end = self.page * 10 + 10
        
        dates = '\n'.join([dt.datetime.strftime(date, "%Y-%m-%d") for date in self.data.index][start:end])
        dividens = '\n'.join([f'{float(div):.2f}' for div in self.data['Dividends']][start:end])
        splits = '\n'.join([f'{float(spl):.2f}' for spl in self.data['Stock Splits']][start:end])

        my_embed = Embed(
            title='More info',
            url=f'{YAHOO_FINANCE_URL}{self.ticker}',
            colour=Colour.blue(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'{self.ticker} | Page {self.page + 1} / {ceil(self.size / 10)}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(name='Date', value=f'```\n{dates}```', inline=True)
        my_embed.add_field(name='Dividens', value=f'```\n{dividens}```', inline=True)
        my_embed.add_field(name='Stock Splits', value=f'```\n{splits}```', inline=True)

        await interaction.response.edit_message(embed=my_embed, view=self)
    

    @button(label='Go to page', style=ButtonStyle.success)
    async def go_to_page_button(self, interaction: Interaction, button: Button) -> None:
        my_modal = MyModalActions(view=self)

        await interaction.response.send_modal(my_modal)