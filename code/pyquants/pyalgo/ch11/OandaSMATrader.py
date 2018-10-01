#
# Python Script
# with Momentum Trading Class
# for Oanda
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import q
import zmq
import numpy as np
import pandas as pd
import oandapy as opy
import datetime as dt
import configparser

# loading credentials
config = configparser.ConfigParser()
config.read('pyalgo.cfg')

oanda = opy.API(environment='practice',
                access_token=config['oanda']['access_token'])

# setting up socket server
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:5555')


class SMATrader(opy.Streamer):
    def __init__(self, instrument, interval, SMA1, SMA2, units, *args, **kwargs):
        opy.Streamer.__init__(self, *args, **kwargs)
        self.ticks = 0
        self.position = 0
        self.data = pd.DataFrame()
        self.instrument = instrument
        self.interval = interval
        self.SMA1 = SMA1
        self.SMA2 = SMA2
        self.units = units

    def create_order(self, side, units):
        order = oanda.create_order(config['oanda']['account_number'],
                                   instrument=self.instrument,
                                   units=units,
                                   side=side,
                                   type='market')
        # order data
        socket.send_string('SMA\n' + str(order))
        print('\n', order)
        q(order)
        # market data
        msg = 'SMA | Market data:\n%s' % self.resam.iloc[-1]
        socket.send_string(msg)
        print('\n', msg)
        q(msg)


    def on_success(self, data):
        self.ticks += 1
        msg = 'SMA | %s | retrieved new data | %5d' % (str(dt.datetime.now()),
                                                       self.ticks)
        socket.send_string(msg)
        print(msg)
        self.data = self.data.append(pd.DataFrame(data['tick'],
                                     index=[data['tick']['time']]))
        self.data.index = pd.DatetimeIndex(self.data['time'])
        self.resam = self.data.resample(self.interval).last()
        if len(self.resam) > self.SMA2:
            self.resam['mid'] = (self.resam['bid'] +
                                 self.resam['ask']) / 2
            self.resam['SMA1'] = self.resam['mid'].rolling(self.SMA1).mean()
            self.resam['SMA2'] = self.resam['mid'].rolling(self.SMA2).mean()
            self.resam['position'] = np.where(self.resam['SMA1'] >
                                              self.resam['SMA2'], 1, -1)
            if self.resam['position'].ix[-1] == 1:
                if self.position == 0:
                    self.create_order('buy', self.units)
                elif self.position == -1:
                    self.create_order('buy', self.units * 2)
                self.position = 1
            elif self.resam['position'].ix[-1] == -1:
                if self.position == 0:
                    self.create_order('sell', self.units)
                elif self.position == 1:
                    self.create_order('sell', self.units * 2)
                self.position = -1
            if self.ticks == 2500:
                if self.position == 1:
                    self.create_order('sell', self.units)
                elif self.position == -1:
                    self.create_order('buy', self.units)
                self.disconnect()

    def on_error(self):
        socket.send_string('A serious error occured.')
        print('\nA serious error occured.')
        q('A serious error occured.')
        # initiate any required/desired risk mitigation task
        self.disconnect()

if __name__ == '__main__':
    sma = SMATrader(instrument='SPX500_USD', interval='10s',
                    SMA1=5, SMA2=10, units=10, environment='practice',
                    access_token=config['oanda']['access_token'])
    sma.rates(account_id=config['oanda']['account_number'],
              instruments=['SPX500_USD'], ignore_heartbeat=True)
