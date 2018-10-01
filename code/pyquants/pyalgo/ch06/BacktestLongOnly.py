#
# Python Script with Long Only Class
# for Event-based Backtesting
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
from BacktestBase import *


class BacktestLongOnly(BacktestBase):

    def run_sma_strategy(self, SMA1, SMA2):
        ''' Backtesting a SMA-based strategy.

        Parameters
        ==========
        SMA1, SMA2: int
            shorter and longer term simple moving average (in days)
        '''
        msg = '\n\nRunning SMA strategy | SMA1 = %d & SMA2 = %d' % (SMA1, SMA2)
        msg += '\nfixed costs %.2f | ' % self.ftc
        msg += 'proportional costs %.4f' % self.ptc
        print(msg)
        print('=' * 55)
        self.position = 0  # initial neutral position
        self.amount = self._amount  # reset initial capital
        self.data['SMA1'] = self.data['price'].rolling(SMA1).mean()
        self.data['SMA2'] = self.data['price'].rolling(SMA2).mean()

        for bar in range(len(self.data)):
            if bar >= SMA2:
                if self.position == 0:
                    if self.data['SMA1'].ix[bar] > self.data['SMA2'].ix[bar]:
                        self.place_buy_order(bar, amount=self.amount)
                        self.position = 1  # long position
                elif self.position == 1:
                    if self.data['SMA1'].ix[bar] < self.data['SMA2'].ix[bar]:
                        self.place_sell_order(bar, units=self.units)
                        self.position = 0  # market neutral
        self.close_out(bar)

    def run_momentum_strategy(self, momentum):
        ''' Backtesting a momentum-based strategy.

        Parameters
        ==========
        momentum: int
            number of days for mean return calculation
        '''
        msg = '\n\nRunning momentum strategy | %d days' % momentum
        msg += '\nfixed costs %.2f | ' % self.ftc
        msg += 'proportional costs %.4f' % self.ptc
        print(msg)
        print('=' * 55)
        self.position = 0  # initial neutral position
        self.amount = self._amount  # reset initial capital

        self.data['momentum'] = self.data['return'].rolling(momentum).mean()

        for bar in range(len(self.data)):
            if bar >= momentum:
                if self.position == 0:
                    if self.data['momentum'].ix[bar] > 0:
                        self.place_buy_order(bar, amount=self.amount)
                        self.position = 1  # long position
                elif self.position == 1:
                    if self.data['momentum'].ix[bar] <= 0:
                        self.place_sell_order(bar, units=self.units)
                        self.position = 0  # market neutral
        self.close_out(bar)

    def run_mean_reversion_strategy(self, SMA, threshold):
        ''' Backtesting a mean reversion-based strategy.

        Parameters
        ==========
        SMA: int
            simple moving average in days
        threshold: float
            absolute value for deviation-based signal relative to SMA
        '''
        msg = '\n\nRunning mean reversion strategy | SMA %d & thr %d' \
            % (SMA, threshold)
        msg += '\nfixed costs %.2f | ' % self.ftc
        msg += 'proportional costs %.4f' % self.ptc
        print(msg)
        print('=' * 55)
        self.position = 0
        self.amount = self._amount

        self.data['SMA'] = self.data['price'].rolling(SMA).mean()

        for bar in range(len(self.data)):
            if bar >= SMA:
                if self.position == 0:
                    if (self.data['price'].ix[bar] <
                            self.data['SMA'].ix[bar] - threshold):
                        self.place_buy_order(bar, amount=self.amount)
                        self.position = 1
                elif self.position == 1:
                    if self.data['price'].ix[bar] >= self.data['SMA'].ix[bar]:
                        self.place_sell_order(bar, units=self.units)
                        self.position = 0
        self.close_out(bar)


if __name__ == '__main__':
    def run_strategies():
        lobt.run_sma_strategy(42, 252)
        lobt.run_momentum_strategy(60)
        lobt.run_mean_reversion_strategy(50, 5)
    lobt = BacktestLongOnly('AAPL', '2010-1-1', '2016-10-31', 10000)
    lobt.verbose = True
    run_strategies()
    lobt = BacktestLongOnly('AAPL', '2010-1-1', '2016-10-31',
                            10000, 10.0, 0.005)  # 10 USD fix, 0.5% variable
    lobt.verbose = False
    run_strategies()
