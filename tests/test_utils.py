import pytest
from yfinance import Ticker

from utils.utils import *


@pytest.mark.parametrize(
    ('ticker'),
    [
        'MSFT',
        'AAPL',
        'NVDA',
        'AMZN',
        'GOOG',
        'META',
        'LLY',
        'TSM',
        'TSLA',
        'TM',
        'SHOP',
        'MDLZ'
    ]
)
def test_fetch_data_valid_ticker(ticker: str) -> None:
    data = fetch_data(ticker)
    
    assert isinstance(data, Ticker)

    assert data.info is not None


@pytest.mark.parametrize(
    ('ticker'),
    [
        '',
        '#MSFT',
        '#META',
        '####',
        'INVALID_TICKER',
        '123abcd',
        '1AAPL'
    ]
)
def test_fetch_data_http_error(ticker: str) -> None:
    with pytest.raises(Exception):
        fetch_data(ticker)