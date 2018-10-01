#
# Python Script
# to Plot Streaming Data
# (Single Stream)
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import zmq
import datetime
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
stream = Stream(maxpoints=100, token=api_tokens[0])
trace = Scatter(x=[], y=[], name='tick data',
                mode='lines+markers', stream=stream)
data = Data([trace])
layout = Layout(title='Apple stock price')
fig = Figure(data=data, layout=layout)
ply.plot(fig, filename='stream_plot', auto_open=True)

s0 = ply.Stream(api_tokens[0])
s0.open()

while True:
    data = socket.recv_string()
    t = datetime.datetime.now()
    print(data)
    sym, value = data.split()
    s0.write({'x': t, 'y': float(value)})
