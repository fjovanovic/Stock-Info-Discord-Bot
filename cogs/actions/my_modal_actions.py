import datetime as dt
from math import ceil

from discord import (
    TextStyle, 
    Interaction, 
    Embed, 
    Colour
)
from discord.ui import Modal, TextInput, View

from utils import errors
from constants import YAHOO_FINANCE_URL


class MyModalActions(Modal, title='Go to page'):
    answer = TextInput(
        label='Enter page number?',
        style=TextStyle.short,
        placeholder='Page?',
        required=True
    )

    def __init__(self, view: View) -> None:
        super().__init__()
        self.view = view
    

    async def on_submit(self, interaction: Interaction) -> None:
        try:
            answer_page = int(self.answer.value)
            if answer_page < 1 or answer_page > ceil(self.view.size / 10):
                await errors.error_embed(
                    interaction,
                    '⛔Wrong page',
                    'Page doesn\'t exist'
                )
                return
        except:
            await errors.error_embed(
                interaction,
                '⛔Wrong input',
                'Enter page number please'
            )
            return
        
        self.view.page = answer_page - 1
        
        if self.view.children[0].disabled == True:
            self.view.children[0].disabled = False
        
        if answer_page == ceil(self.view.size / 10):
            self.view.children[1].disabled = True
        elif self.view.children[1].disabled == True:
            self.view.children[1].disabled = False
        
        start = self.view.page * 10
        end = self.view.page * 10 + 10
        
        dates = '\n'.join([dt.datetime.strftime(date, "%Y-%m-%d") for date in self.view.data.index][start:end])
        dividens = '\n'.join([f'{float(div):.2f}' for div in self.view.data['Dividends']][start:end])
        splits = '\n'.join([f'{float(spl):.2f}' for spl in self.view.data['Stock Splits']][start:end])

        my_embed = Embed(
            title='More info',
            url=f'{YAHOO_FINANCE_URL}{self.view.ticker}',
            colour=Colour.blue(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'{self.view.ticker} | Page {answer_page} / {ceil(self.view.size / 10)}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(name='Date', value=f'```\n{dates}```', inline=True)
        my_embed.add_field(name='Dividens', value=f'```\n{dividens}```', inline=True)
        my_embed.add_field(name='Stock Splits', value=f'```\n{splits}```', inline=True)
        
        await interaction.response.edit_message(embed=my_embed, view=self.view)