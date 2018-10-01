#
# Python Script
# with Tick Data Server
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import zmq
import math
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:5555')


class StockPrice(object):
    def __init__(self):
        self.symbol = 'AAPL'
        self.t = time.time()
        self.value = 100.
        self.sigma = 0.4
        self.r = 0.05

    def simulate_value(self):
        ''' Generates a new, random stock price.
        '''
        t = time.time()
        dt = (t - self.t) / (252 * 8 * 60 * 60)
        dt *= 100
        self.t = t
        self.value *= math.exp((self.r - 0.5 * self.sigma ** 2) * dt +
                        self.sigma * math.sqrt(dt) * random.gauss(0, 1))
        return self.value


sp = StockPrice()

while True:
    msg = '%s %s' % (sp.symbol, sp.simulate_value())
    print(msg)
    socket.send_string(msg)
    time.sleep(random.random())
