#
# Python Module with Class
# for Vectorized Backtesting
# of Momentum-based Strategies
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import numpy as np
import pandas as pd
from pandas_datareader import data as web
import quandl as q

class MomVectorBacktester(object):
    ''' Class for the vectorized backtesting of
    Momentum-based trading strategies.

    Attributes
    ==========
    symbol: str
        Google Finance symbol with which to work with
    start: str
        start date for data retrieval
    end: str
        end date for data retrieval
    amount: int, float
        amount to be invested at the beginning
    tc: float
        proportional transaction costs (e.g. 0.5% = 0.005) per trade

    Methods
    =======
    get_data:
        retrieves and prepares the base data set
    run_strategy:
        runs the backtest for the momentum-based strategy
    plot_results:
        plots the performance of the strategy compared to the symbol
    '''

    def __init__(self, symbol, start, end, amount, tc):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.amount = amount
        self.tc = tc
        self.results = None
        self.quandl_api_key = 'tazR87u-Jc7PsHZ2XV1-'
        self.get_data()

    def get_data(self):
        ''' Retrieves and prepares the data.
        '''
        '''
        raw = web.DataReader(self.symbol, data_source='google',
                             start=self.start, end=self.end)['Close']
        '''
        raw = q.get('WIKI/'+self.symbol, start_date=self.start, end_date=self.end, api_key=self.quandl_api_key)['Adj. Close']
        raw = pd.DataFrame(raw)
        raw.rename(columns={'Adj. Close': 'price'}, inplace=True)
        raw['return'] = np.log(raw / raw.shift(1))
        self.data = raw

    def run_strategy(self, momentum=1):
        ''' Backtests the trading strategy.
        '''
        self.momentum = momentum
        data = self.data.copy()
        data['position'] = np.sign(data['return'].rolling(momentum).mean())
        data['strategy'] = data['position'].shift(1) * data['return']
        # determine when a trade takes place
        trades = data['position'].diff().fillna(0) != 0
        # subtract transaction costs from return when trade takes place
        data['strategy'][trades] -= self.tc
        data['creturns'] = self.amount * data['return'].cumsum().apply(np.exp)
        data['cstrategy'] = self.amount * \
            data['strategy'].cumsum().apply(np.exp)
        self.results = data
        # absolute performance of the strategy
        aperf = self.results['cstrategy'].ix[-1]
        # out-/underperformance of strategy
        operf = aperf - self.results['creturns'].ix[-1]
        return round(aperf, 2), round(operf, 2)

    def plot_results(self):
        ''' Plots the cumulative performance of the trading strategy
        compared to the symbol.
        '''
        if self.results is None:
            print('No results to plot yet. Run a strategy.')
        title = '%s | TC = %.4f' % (self.symbol, self.tc)
        self.results[['creturns', 'cstrategy']].plot(title=title,
                                                     figsize=(10, 6))


if __name__ == '__main__':
    mombt = MomVectorBacktester('AAPL', '2010-1-1', '2016-10-31', 10000, 0.0)
    print(mombt.run_strategy())
    print(mombt.run_strategy(momentum=2))
    mombt = MomVectorBacktester('AAPL', '2010-1-1', '2016-10-31', 10000, 0.001)
    print(mombt.run_strategy(momentum=2))
