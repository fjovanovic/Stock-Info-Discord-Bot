import datetime as dt

from discord import (
    TextStyle, 
    Interaction, 
    Embed, 
    Colour
)
from discord.ui import TextInput, View

from components import MyModal
from utils import errors


class MyModalInstitutionalHolders(MyModal, title='Go to page'):
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
            if answer_page < 1 or answer_page > self.view.size:
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
        
        self.view.page = answer_page        
        
        if self.view.children[0].disabled == True:
            self.view.children[0].disabled = False
        
        if answer_page == self.view.size:
            self.view.children[1].disabled = True
        elif self.view.children[1].disabled == True:
            self.view.children[1].disabled = False

        my_embed = Embed(
            color=Colour.green(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'Page {answer_page} / {self.view.size}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(
            name='Holder', 
            value=f'`{self.view.data.iloc[answer_page - 1]["Holder"]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Shares', 
            value=f'`{self.view.data.iloc[answer_page - 1]["Shares"]:,}`', 
            inline=False
        )
        my_embed.add_field(
            name='Date Reported', 
            value=f'`{self.view.data.iloc[answer_page - 1]["Date Reported"]}`', 
            inline=False
        )
        my_embed.add_field(
            name='% held', 
            value=f'`{self.view.data.iloc[answer_page - 1]["pctHeld"]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Value', 
            value=f'`{self.view.data.iloc[answer_page - 1]["Value"]:,} $`', 
            inline=False
        )
        
        await interaction.response.edit_message(embed=my_embed, view=self.view)