import plotly.plotly as py
import plotly.graph_objs as go

import pandas_datareader as web
from datetime import datetime

start = datetime(2010, 1, 1)
end = datetime(2013, 1, 27)
df = web.DataReader("gs", 'google', datetime(2008, 1, 1), datetime(2008, 12, 28))
# df = web.DataReader("aapl", 'yahoo', start, end)

trace = go.Candlestick(x=df.index,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close)
data = [trace]
py.iplot(data, filename='simple_candlestick')