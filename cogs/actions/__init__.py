from components import MyBot
from .actions import Actions


async def setup(bot: MyBot) -> None:
    await bot.add_cog(Actions(bot=bot))