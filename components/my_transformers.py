from discord import Interaction
from discord.app_commands import Transformer


class TransformUpper(Transformer):
    async def transform(self, interaction: Interaction, value: str) -> str:
        return value.upper()