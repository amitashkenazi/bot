import requests
import json
from mpl_finance import candlestick_ohlc
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
import numpy as np
import pyperclip

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

    for k, v in parameters.iteritems():
        build_command += k + "=" + v + "&"
    build_command = build_command[:-1]
    r_type = dict
    


    if command == "klines":
        r_type = list
    r = requests.get('https://api.binance.com/api/v1/' + build_command)
    data = r_type(json.loads(r.content))
    return {"data": data, "type": r_type}

