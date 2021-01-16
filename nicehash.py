import requests
import json
from scipy.signal import medfilt
import time
import datetime

id = 757104

api_key = "af991536-cbb7-a2ab-bed3-24a9d8209eef"
readonly_api_key = "c46bd50e-8c60-cbcf-1884-37b4e21de967"
orders_get = "https://api.nicehash.com/api?method=orders.get&location=0&algo={algo}".format(algo=20)
my_orders_get = "https://api.nicehash.com/api?method=orders.get&my&id={id}&key={key}&location=0&algo={algo}".format(id=id, key=readonly_api_key, algo=20)

while 1:
    print "sleeping.... ({})".format(datetime.datetime.now().time())
    time.sleep(60*10)
    print "checking prices"
    res = requests.get(orders_get)
    data = dict(json.loads(res.content))
    # for d in data["result"]["orders"]:
    #     print d["id"], d["workers"], d["price"], d["type"]

    workers = []
    price = []
    price_count = {}
    for r in data["result"]["orders"]:
        if r["type"] == 1:
            continue
        workers.append(r["workers"])
        if r['price'] not in price_count:
            price_count[r['price']] = 0
        if r["workers"] > 0:
            price_count[r['price']] += 1
        price.append(r['price'])
    for k in sorted(price_count.keys()):
        # print k, price_count[k]
        if price_count[k] > 8:
            calc_price = k
            break
    res = requests.get(my_orders_get)
    data = dict(json.loads(res.content))
    order_id = data["result"]["orders"][0]["id"]
    order_price = data["result"]["orders"][0]["price"]
    print "the new desired price is {} current price is {}".format(k, order_price)
    if calc_price < order_price:
        print "decreasing the order price"
        command = "https://api.nicehash.com/api?method=orders.set.price.decrease&id={id}&key={key}&location=0&algo={algo}&order={order}".format(id=id, key=api_key, algo=20, order=order_id)
    elif calc_price > order_price:
        print "increasing the order price to {}".format(calc_price)
        command = "https://api.nicehash.com/api?method=orders.set.price&id={id}&key={key}&location=0&algo={algo}&order={order}&price={price}".format(id=id, key=api_key, algo=20, order=order_id, price=calc_price)
    else:
        print "no change in price"
        continue
    res = requests.get(command)
    data = dict(json.loads(res.content))
    print data



