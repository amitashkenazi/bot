import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import ast
import logging
from pprint import pprint
logger = logging.getLogger(__name__)

kline_return_struct = [
        "Open time", #0
        "Open", #1
        "High", #2
        "Low", #3
        "Close", #4
        "Volume", #5
        "Close time", #6
        "Quote asset volume", #7
        "Number of trades", #8
        "Taker buy base asset volume", #9
        "Taker buy quote asset volume", #10
        "Ignore", #11
    ]

def command_request(command, parameters):
    build_command = command + "?"

    for k, v in parameters.items():
        build_command += k + "=" + v + "&"
    build_command = build_command[:-1]
    r_type = dict
    if command == "klines":
        r_type = list
    r = requests.get('https://api.binance.com/api/v1/' + build_command)
    data = r_type(json.loads(r.content))
    if len(data) == 0:
        return {"data": [], "type": r_type, "error": -2}
    if str(data[1]) == 'code':
        print("coin not found")
        return {"data": [], "type": None, "error": -1}
    return {"data": data, "type": r_type, "error": 0}

def get_exchange_info():
    r = requests.get('https://api.binance.com/api/v1/exchangeInfo')
    data = dict(json.loads(r.content))
    return data

def get_symbols():
    info =  get_exchange_info()
    r_symbols = info["symbols"]
    symbols = []
    for s in r_symbols:
        symbols.append(s["symbol"])
    return symbols

def marketcaps():
    # response_struct = ["id", "name", "symbol", "rank", "price_usd", "price_btc", "24h_volume_usd", "market_cap_usd", "available_supply", "total_supply", "max_supply", "percent_change_1h", "percent_change_24h", "percent_change_7d", "last_updated"]
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'dc5b9509-4fdd-474b-8317-88ed3d5b4bf6',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    logger.info(data.keys())
    logger.info(len(data["data"]))
    for d in data["data"]:
        logger.info(f"{d['name']} - {d['quote']['USD']['market_cap']}")
    return data



if __name__ == "__main__":
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)15s:: %(filename)18s:%(lineno)d  :  %(message)s" 
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    logger.info(marketcaps())
    # logger.info(get_symbols())