import os
import discord
from dotenv import load_dotenv
from argparse import ArgumentParser
import asyncio

from components import MyBot, MyCommandTree
from utils import utils


load_dotenv()

bot = MyBot(command_prefix='$', activity_name='Stock market', tree_cls=MyCommandTree)


async def main():
    parser = ArgumentParser(
        usage='python3 main.py [-t | --test]',
        description='Discord bot for providing stock information',
        allow_abbrev=False
    )

    parser.add_argument('-t', '--test', action='store_true', help='Providing console log instead of file log')
    args = parser.parse_args()
    if args.test:
        discord.utils.setup_logging()
    else:
        utils.setup_file_logging()
    
    TOKEN = os.getenv('TOKEN')
    await bot.start(TOKEN)


asyncio.run(main())