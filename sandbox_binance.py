import requests
import json
import mplfinance 
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
import numpy as np
import pyperclip
from api_binance import command_request

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

def sma(values, weights):
    """ Numpy implementation of EMA
    """
    weights = np.ones(window)
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='valid')[:len(values)]
    a[:window] = a[window]
    return a

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

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    print(event.xdata) 
    pyperclip.copy("{}".format(int(event.xdata)))

command = 'klines'

parameters = {
    "symbol":"CNDBTC",
    "interval": "5m",
    "limit": "500",
    # "startTime": "1506964411",
    # "endTime": "1507223611",
}

res = command_request(command, parameters)
data = res["data"]
quote = []
# time, open, high, low, close
opens = []
closes = []
times = []

print(len(data))
for d in data:
    times.append(int(d[0])/1000)
    opens.append(float(d[1]))
    closes.append(float(d[4]))
    quote.append([
        int(d[0])/1000,
        float(d[1]),
        float(d[2]),
        float(d[3]),
        float(d[4]),
        ]

        )
mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays = DayLocator()              # minor ticks on the days
weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
dayFormatter = DateFormatter('%d')      # e.g., 12
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)

window = 24 # slow
EMA1 = exp_moving_average(closes, window)
# EMA1 = np.array(sma(closes, window))

window = 12
EMA2 = exp_moving_average(closes, window)
# EMA2 = np.array(sma(closes, window))


