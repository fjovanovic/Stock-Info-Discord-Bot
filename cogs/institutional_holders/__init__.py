from components import MyBot
from .institutional_holders import InstitutionalHolders


async def setup(bot: MyBot) -> None:
    await bot.add_cog(InstitutionalHolders(bot=bot))