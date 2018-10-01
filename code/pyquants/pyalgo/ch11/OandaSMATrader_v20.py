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
import v20
import zmq
import numpy as np
import pandas as pd
import datetime as dt
import configparser

# loading credentials
config = configparser.ConfigParser()
config.read('pyalgo.cfg')

# setting up socket server
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:5555')

class SMATrader(object):
    def __init__(self, instrument, interval, SMA1, SMA2, units,
                 *args, **kwargs):
        self.ticks = 0
        self.position = 0
        self.data = pd.DataFrame()
        self.instrument = instrument
        self.interval = interval
        self.SMA1 = SMA1
        self.SMA2 = SMA2
        self.units = units
        self.account_id = config['oanda_v20']['account_id']
        self.ctx = v20.Context(
            'api-fxpractice.oanda.com',
            443,
            True,
            application='sample_code',
            token=config['oanda_v20']['access_token'],
            datetime_format='RFC3339'
        )
        self.ctx_stream = v20.Context(
            'stream-fxpractice.oanda.com',
            443,
            True,
            application='sample_code',
            token=config['oanda_v20']['access_token'],
            datetime_format='RFC3339'
        )

    def start(self):
        response = self.ctx_stream.pricing.stream(
            self.account_id,
            snapshot=True,
            instruments=self.instrument
        )
        for msg_type, msg in response.parts():
            if msg_type == 'pricing.Price':
                self.on_success(msg.time, msg.bids[0].price, msg.asks[0].price)
            if self.ticks == 500:
                if self.position == 1:
                    self.create_order(-self.units)
                elif self.position == -1:
                    self.create_order(self.units)
                return 'Finished'

    def create_order(self, units):
        request = self.ctx.order.market(
            self.account_id,
            instrument=self.instrument,
            units=units,
        )
        order = request.get('orderFillTransaction')
        # order data
        socket.send_string('SMA\n' + str(order))
        print('\n', str(order))
        q(str(order))
        # market data
        msg = 'SMA | Market data:\n%s' % self.resam.iloc[-1]
        socket.send_string(msg)
        print('\n', msg)
        q(msg)

    def on_success(self, time, bid, ask):
        self.ticks += 1
        msg = 'SMA | %s | retrieved new data | %5d' % (str(dt.datetime.now()),
                                                       self.ticks)
        socket.send_string(msg)
        print(msg)
        self.data = self.data.append(
            pd.DataFrame({'time': [time], 'bid': [bid], 'ask': [ask]}))
        self.data.index = pd.DatetimeIndex(self.data['time'])
        self.resam = self.data.resample(self.interval).last().ffill()
        if len(self.resam) > self.SMA2:
            self.resam['mid'] = (self.resam['bid'] +
                                 self.resam['ask']) / 2
            self.resam['SMA1'] = self.resam['mid'].rolling(self.SMA1).mean()
            self.resam['SMA2'] = self.resam['mid'].rolling(self.SMA2).mean()
            self.resam['position'] = np.where(self.resam['SMA1'] >
                                              self.resam['SMA2'], 1, -1)
            # print(self.resam[['bid', 'ask', 'SMA1', 'SMA2',
            #                   'position']].tail())
            if self.resam['position'].ix[-1] == 1:
                if self.position == 0:
                    self.create_order(self.units)
                elif self.position == -1:
                    self.create_order(self.units * 2)
                self.position = 1
            elif self.resam['position'].ix[-1] == -1:
                if self.position == 0:
                    self.create_order(-self.units)
                elif self.position == 1:
                    self.create_order(-self.units * 2)
                self.position = -1

    def on_error(self):
        ''' Call this method in case of any error/exception. '''
        socket.send_string('A serious error occured.')
        print('\nA serious error occured.')
        q('A serious error occured.')
        # initiate any required/desired risk mitigation task

if __name__ == '__main__':
    sma = SMATrader(instrument='DE30_EUR', interval='10s',
                    SMA1=5, SMA2=10, units=10)
    sma.start()
