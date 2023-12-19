from discord.ext.commands import CommandError


class YfinanceHTTPError(CommandError):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)