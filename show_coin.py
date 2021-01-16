from pymongo import MongoClient
import matplotlib.pyplot as plt
import pyperclip
import numpy as np

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    print event.xdata 
    pyperclip.copy("{}".format(int(event.xdata)))

def exp_moving_average(values, window):
    """ Numpy implementation of EMA
    """
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='valid')[:len(values)]
    a[:window] = a[window+1]
    z = np.ones(len(values)-len(a)) * a[0]
    a = np.concatenate((z,a))
    return a


url = '127.0.0.1'
client = MongoClient(url, ssl=False)
connection = client['binance_coins']

symbol = 'ETHBTC'
coins_collection = connection[symbol]

res = coins_collection.find({})
closes = []
times = []
for r in res:
    closes.append(r["Close"])
    times.append(r["Close time"])

print len(closes)

window = 24 # slow
EMA1 = exp_moving_average(closes, window)
# EMA1 = np.array(sma(closes, window))

window = 12
EMA2 = exp_moving_average(closes, window)



fig, ax3 = plt.subplots()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.plot(times, closes)
plt.plot(times, EMA1, color='g')
plt.plot(times, EMA2, color='r')

plt.show()