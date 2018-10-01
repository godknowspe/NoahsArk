#
# Python Script with Long Short Class
# for Event-based Backtesting
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
from BacktestBase import *


class BacktestLongShort(BacktestBase):

    def go_long(self, bar, units=None, amount=None):
        if self.position == -1:
            self.place_buy_order(bar, units=self.units)
        if units:
            self.place_buy_order(bar, units=units)
        elif amount:
            if amount == 'all':
                amount = self.amount
            self.place_buy_order(bar, amount=amount)

    def go_short(self, bar, units=None, amount=None):
        if self.position == 1:
            self.place_sell_order(bar, units=self.units)
        if units:
            self.place_sell_order(bar, units=units)
        elif amount:
            if amount == 'all':
                amount = self.amount
            self.place_sell_order(bar, amount=amount)

    def run_sma_strategy(self, SMA1, SMA2):
        msg = '\n\nRunning SMA strategy | SMA1 = %d & SMA2 = %d' % (SMA1, SMA2)
        msg += '\nFixed costs %.2f | ' % self.ftc
        msg += 'proportional costs %.4f' % self.ptc
        print(msg)
        print('=' * 55)
        self.position = 0  # initial neutral position
        self.amount = self._amount  # reset initial capital
        self.data['SMA1'] = self.data['price'].rolling(SMA1).mean()
        self.data['SMA2'] = self.data['price'].rolling(SMA2).mean()

        for bar in range(len(self.data)):
            if bar >= SMA2:
                if self.position in [0, -1]:
                    if self.data['SMA1'].ix[bar] > self.data['SMA2'].ix[bar]:
                        self.go_long(bar, amount='all')
                        self.position = 1  # long position
                elif self.position in [0, 1]:
                    if self.data['SMA1'].ix[bar] < self.data['SMA2'].ix[bar]:
                        self.go_short(bar, amount='all')
                        self.position = -1  # short position
        self.close_out(bar)

    def run_momentum_strategy(self, momentum):
        msg = '\n\nRunning momentum strategy | %d days' % momentum
        msg += '\nFixed costs %.2f | ' % self.ftc
        msg += 'proportional costs %.4f' % self.ptc
        print(msg)
        print('=' * 55)
        self.position = 0  # initial neutral position
        self.amount = self._amount  # reset initial capital

        self.data['momentum'] = self.data['return'].rolling(momentum).mean()

        for bar in range(len(self.data)):
            if bar >= momentum:
                if self.position in [0, -1]:
                    if self.data['momentum'].ix[bar] > 0:
                        self.go_long(bar, amount='all')
                        self.position = 1  # long position
                elif self.position in [0, 1]:
                    if self.data['momentum'].ix[bar] <= 0:
                        self.go_short(bar, amount='all')
                        self.position = -1  # long position
        self.close_out(bar)

    def run_mean_reversion_strategy(self, SMA, threshold):
        msg = '\n\nRunning mean reversion strategy | SMA %d & thr %d' \
            % (SMA, threshold)
        msg += '\nFixed costs %.2f | ' % self.ftc
        msg += 'proportional costs %.4f' % self.ptc
        print(msg)
        print('=' * 55)
        self.position = 0  # initial neutral position
        self.amount = self._amount  # reset initial capital

        self.data['SMA'] = self.data['price'].rolling(SMA).mean()

        for bar in range(len(self.data)):
            if bar >= SMA:
                if self.position == 0:
                    if (self.data['price'].ix[bar] <
                            self.data['SMA'].ix[bar] - threshold):
                        self.go_long(bar, amount=self._amount)
                        self.position = 1
                    elif (self.data['price'].ix[bar] >
                            self.data['SMA'].ix[bar] + threshold):
                        self.go_short(bar, amount=self._amount)
                        self.position = -1
                elif self.position == 1:
                    if self.data['price'].ix[bar] >= self.data['SMA'].ix[bar]:
                        self.place_sell_order(bar, units=self.units)
                        self.position = 0
                elif self.position == -1:
                    if self.data['price'].ix[bar] <= self.data['SMA'].ix[bar]:
                        self.place_buy_order(bar, units=-self.units)
                        self.position = 0
        self.close_out(bar)


if __name__ == '__main__':
    def run_strategies():
        lobt.run_sma_strategy(42, 252)
        lobt.run_momentum_strategy(60)
        lobt.run_mean_reversion_strategy(50, 5)
    lobt = BacktestLongShort('AAPL', '2010-1-1', '2016-10-31', 10000)
    lobt.verbose = True
    run_strategies()
    lobt = BacktestLongShort('AAPL', '2010-1-1', '2016-10-31',
                             10000, 10.0, 0.005)  # 10 USD fix, 0.5% variable
    lobt.verbose = False
    run_strategies()
