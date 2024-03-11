import datetime as dt

from discord import Interaction, Embed, Colour
from discord.ui import Select


class MySelectInstitutionalHolders(Select):
    def __init__(self, data: dict) -> None:
        super().__init__(
            placeholder='Get more about institutional holder',
            min_values=1,
            max_values=1
        )
        self.data = data
    

    async def callback(self, interaction: Interaction) -> None:
        index = int(self.values[0])

        my_embed = Embed(
            color=Colour.green(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'Information about institutional holder', icon_url=interaction.user.avatar.url)
        my_embed.add_field(
            name='Holder', 
            value=f'`{self.data.iloc[index]["Holder"]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Shares', 
            value=f'`{self.data.iloc[index]["Shares"]:,}`', 
            inline=False
        )
        my_embed.add_field(
            name='Date Reported', 
            value=f'`{self.data.iloc[index]["Date Reported"]}`', 
            inline=False
        )
        my_embed.add_field(
            name='% held', 
            value=f'`{self.data.iloc[index]["pctHeld"]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Value', 
            value=f'`{self.data.iloc[index]["Value"]:,} $`', 
            inline=False
        )

        await interaction.response.send_message(embed=my_embed)