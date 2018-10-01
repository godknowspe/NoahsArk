#
# Python Script
# with SMA Trading Class
# for Interactive Brokers
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import tpqib
import pandas as pd
import datetime as dt


class SMATrader(object):
    def __init__(self, symbol, shares):
        self.con = tpqib.tpqibcon()
        self.symbol = symbol
        self.shares = shares
        self.contract = self.con.create_contract(symbol, 'STK', 'SMART',
                                                 'SMART', 'USD')
        self.details = self.con.req_contract_details(self.contract)
        self.buy_order = self.con.create_order('MKT', shares, 'Buy')
        self.sell_order = self.con.create_order('MKT', shares, 'Sell')
        self.data = pd.DataFrame()
        self.ticks = 0

    def define_strategy(self, field, value):
        self.ticks += 1
        if field == 'bidPrice':
            timestamp = dt.datetime.now()
            self.data = self.data.append(pd.DataFrame({'bid': value},
                                                      index=[timestamp]))
            print(timestamp, '| bid is %s' % value)
        elif field == 'askPrice':
            timestamp = dt.datetime.now()
            self.data = self.data.append(pd.DataFrame({'ask': value},
                                                      index=[timestamp]))
            print(timestamp, '| ask is %s' % value)
        if self.ticks == 50:
            self.con.cancel_market_data(self.request_id)

    def run_strategy(self):
        self.request_id = self.con.request_market_data(self.contract,
                                                       self.define_strategy)


if __name__ == '__main__':
    sma = SMATrader('AAPL', 100)
    sma.run_strategy()
