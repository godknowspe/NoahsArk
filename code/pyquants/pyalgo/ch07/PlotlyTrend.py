#
# Python Script
# to Plot Streaming Data
# (Three Streams)
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import zmq
import datetime
import pandas as pd
import plotly.plotly as ply
from plotly.graph_objs import *
import configparser

# configuration
config = configparser.ConfigParser()
config.read('../pyalgo.cfg')
ply.sign_in(config['plotly']['user_name'], config['plotly']['api_key'])
api_tokens = list(config['plotly']['api_tokens'].split(','))

# socket connection
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://0.0.0.0:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, 'AAPL')

# plotly preparation
stream_0 = Stream(maxpoints=100, token=api_tokens[0])
stream_1 = Stream(maxpoints=100, token=api_tokens[1])
stream_2 = Stream(maxpoints=100, token=api_tokens[2])
trace_0 = Scatter(x=[], y=[], name='tick data',
                  mode='lines+markers', stream=stream_0)
trace_1 = Scatter(x=[], y=[], name='SMA 1',
                  mode='lines', stream=stream_1)
trace_2 = Scatter(x=[], y=[], name='SMA 2',
                  mode='lines', stream=stream_2)
data = Data([trace_0, trace_1, trace_2])
layout = Layout(title='Apple stock price & SMAs')
fig = Figure(data=data, layout=layout)
ply.plot(fig, filename='trend_plot', auto_open=True)

s0 = ply.Stream(api_tokens[0])
s1 = ply.Stream(api_tokens[1])
s2 = ply.Stream(api_tokens[2])
s0.open()
s1.open()
s2.open()

df = pd.DataFrame()

while True:
    data = socket.recv_string()
    t = datetime.datetime.now()
    print(data)
    sym, value = data.split()
    df = df.append(pd.DataFrame({sym: float(value)}, index=[t]))
    df['SMA1'] = df[sym].rolling(5).mean()
    df['SMA2'] = df[sym].rolling(10).mean()
    s0.write({'x': t, 'y': df[sym].ix[-1]})
    s1.write({'x': t, 'y': df['SMA1'].ix[-1]})
    s2.write({'x': t, 'y': df['SMA2'].ix[-1]})
