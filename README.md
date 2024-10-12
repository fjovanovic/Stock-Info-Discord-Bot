# Stock Info Discord Bot  
:warning: **Not an official product**  
The financial data provided by the Bot, sourced through the [yfinance](https://github.com/ranaroussi/yfinance) Python library, is for informational purposes only.  
While the Bot strive to provide accurate and up-to-date information, it doesn't guarantee the accuracy, completeness, or reliability of the data.
The information presented by the Bot is not intended to be financial advice.  
The use of the yfinance Python library and any associated financial data does not imply 
an endorsement or recommendation of any particular financial instrument, investment strategy, or course of action. The Bot's functionality is limited to displaying 
financial data obtained from the mentioned library, it does not execute trades, provide personalized financial advice, or offer real-time market data.

## Prerequisites
* `.env` file
  > Provide `TOKEN` variable obtained from Discord developer portal

* `venv`
  > Before installing dependencies it is highly recommended to work in [virtual environment](https://docs.python.org/3/library/venv.html).
  > If you want to create virtual environment `.venv`, use following command:
  > ```bash
  >  python -m venv .venv
  >  ```
  > Make sure it is activated after installation

## Install dependencies
```bash
pip install -r requirements.txt
```

## Usage
* Command `python main.py`
  > This command initiates the bot using file logging. The bot's activities, errors, and relevant information will be logged into a file named `discord.log`.
  > File logging has advantages for long-term record-keeping, troubleshooting, and maintaining a history of the bot's performance.
  > Keep in mind that file logging may accumulate data over time, so regular maintenance might be needed to manage log files.

* Command `python main.py --test`
  > This command starts the bot in testing mode, utilizing standard console logging. When initiated with the --test flag, the bot will log information
  > directly to the console instead of a file. Console logging is useful during testing and development phases, providing immediate feedback and visibility into the bot's activities.

## Commands
<table>
  <tr>
    <th>Command</th>
    <th>Explanation</th>
  </tr>
  <tr>
    <td>/major_holders</td>
    <td>Major holders for the stock</td>
  </tr>
  <tr>
    <td>/institutional_holders</td>
    <td>Institutional holders for the stock</td>
  </tr>
  <tr>
    <td>/chart</td>
    <td>Chart for the stock and given period and interval</td>
  </tr>
  <tr>
    <td>/earnings_dates</td>
    <td>Future (4) and historic (8) earnings dates</td>
  </tr>
  <tr>
    <td>/actions</td>
    <td>Stock actions (dividens, stock splits)</td>
  </tr>
</table>
