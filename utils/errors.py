from discord import Interaction, Embed, Colour


async def error_embed(interaction: Interaction, name: str, value: str) -> None:
    my_embed = Embed(
        colour=Colour.red()
    )

    my_embed.add_field(name=name, value=value)

    await interaction.followup.send(embed=my_embed)