import csv
from pymongo import MongoClient

input_file = csv.DictReader(open('ETHBTC_1.csv'))
url = '127.0.0.1'
client = MongoClient(url, ssl=False)
connection = client['binance_coins']
coins_collection = connection['ETHBTC']
res = connection['ETHBTC'].find({"symbol":"ETHBTC"})
print (list(res))



docs = []
# print reader
for row in input_file:
    docs.append(row)
    print row


coins_collection.insert(docs)