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
        index = self.values[0]

        my_embed = Embed(
            color=Colour.green(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'Information about institutional holder', icon_url=interaction.user.avatar.url)
        my_embed.add_field(
            name='Holder', 
            value=f'`{self.data["Holder"][str(index)]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Shares', 
            value=f'`{self.data["Shares"][str(index)]:,}`', 
            inline=False
        )
        my_embed.add_field(
            name='Date Reported', 
            value=f'`{dt.datetime.fromtimestamp(self.data["Date Reported"][str(index)] / 1000)}`', 
            inline=False
        )
        my_embed.add_field(
            name='% Out', 
            value=f'`{self.data["% Out"][str(index)]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Value', 
            value=f'`{self.data["Value"][str(index)]:,} $`', 
            inline=False
        )

        await interaction.response.send_message(embed=my_embed)