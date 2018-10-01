#
# Python Script
# with Online Trading Algorithm
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import zmq
import datetime
import numpy as np
import pandas as pd

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://0.0.0.0:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, 'AAPL')

df = pd.DataFrame()

while True:
    data = socket.recv_string()
    t = datetime.datetime.now()
    sym, value = data.split()
    df = df.append(pd.DataFrame({sym: float(value)}, index=[t]))
    dr = df.resample('5s').last()
    dr['returns'] = np.log(dr / dr.shift(1))
    dr['momentum'] = np.sign(dr['returns'].rolling(3).mean())
    print('\n' + '=' * 51)
    print(dr.tail())
    if dr['momentum'].ix[-1] == 1.0:
        print('\nLong market position.')
        # take some action (e.g. place buy order)
    elif dr['momentum'].ix[-1] == -1.0:
        print('\nShort market position.')
        # take some action (e.g. place sell order)
