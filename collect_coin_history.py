from api_binance import command_request, marketcaps
import pyperclip
import time

from pymongo import MongoClient


def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    print event.xdata 
    pyperclip.copy("{}".format(int(event.xdata)))


url = '127.0.0.1'
client = MongoClient(url, ssl=False)
connection = client['binance_coins']


interval = "5m"
# end_time = 1483315200
time_diff_sec = 500 * 300000
fieldtypes = {
        "Open time": long, #0
        "Open": float, #1
        "High": float, #2
        "Low": float, #3
        "Close": float, #4
        "Volume": float, #5
        "Close time": long, #6
        "Quote asset volume": float, #7
        "Number of trades": int, #8
        "Taker buy base asset volume": float, #9
        "Taker buy quote asset volume": float, #10
        "Ignore": float, #11
        }
fieldnames = [
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


start_time = 0
i = 0
# mcs = marketcaps()
mcs = ["ETH"]
for coin in mcs:
    symbol = "{}BTC".format(coin)
    coins_collection = connection[symbol]
    print symbol
    result = connection[symbol].delete_many({})
    end_time = int(time.time()*1000)
    start_time = 1500004618000 + (i*time_diff_sec)
    i = 0 
    while start_time < end_time:
        start_time = 1500004618000 + (i*time_diff_sec)
        i += 1 

        command = 'klines'
        parameters = {
            "symbol":"{}BTC".format(coin),
            "interval": "5m",
            "limit": "500",
            "startTime": str(start_time),
            # "endTime": str(1483315200),
        }
        docs = []
        res = command_request(command, parameters)
        print ".", start_time, end_time
        
        if res["error"] == -1: # no coin found 
            break
        if res["error"] == -2: # no data returned
            continue
        data = res["data"]
        for d in data:
            r = dict(zip(fieldnames, d))
            for k, v in r.iteritems():
                r[k] = fieldtypes[k](v)
            docs.append(r)
        coins_collection.insert(docs)
