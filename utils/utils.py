from yfinance import Ticker
from requests.exceptions import HTTPError
import logging
import logging.handlers

from components.my_errors import *


def setup_file_logging() -> None:
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )

    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def fetch_data(ticker: str) -> Ticker:
    data = Ticker(ticker)

    try:
        if len(data.info.keys()) == 1 and data.info['trailingPegRatio'] is None:
            raise HTTPError
    except HTTPError as e:
        raise YfinanceHTTPError

    return data