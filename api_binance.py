import requests
import json
import ast

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
    if len(data) == 0:
        return {"data": [], "type": r_type, "error": -2}
    if str(data[1]) == 'code':
        print "coin not found"
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
        print s
        symbols.append(s["symbol"])
    return symbols

def marketcaps():
    response_struct = ["id", "name", "symbol", "rank", "price_usd", "price_btc", "24h_volume_usd", "market_cap_usd", "available_supply", "total_supply", "max_supply", "percent_change_1h", "percent_change_24h", "percent_change_7d", "last_updated"]
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/')
    start = False
    resp = {}
    results = []
    for l in r.text.splitlines():
        if l.find(response_struct[0]) > 0:
            start = True
            resp = {}
            idx = 0
        if start:
            key_pos = l.find(response_struct[idx])
            comma_pos = l.find(',')
            resp[response_struct[idx]] = l[key_pos+len(response_struct[idx])+4:comma_pos-1]
            idx += 1
        if l.find(response_struct[-1]) > 0:
            results.append(resp)
            start = False
    market_caps = {}
    for r in results:
        try:
            mc = int(float(r["market_cap_usd"]))
        except:
            print "error coverting market cap"
        else:
            market_caps[str(r["symbol"])] = mc
    return market_caps



