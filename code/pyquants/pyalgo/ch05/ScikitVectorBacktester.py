#
# Python Module with Class
# for Vectorized Backtesting
# of Machine Learning-based Strategies
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import numpy as np
import pandas as pd
from pandas_datareader import data as web
from sklearn import linear_model

h5 = pd.HDFStore('../data/equities.h5', 'r')
data = h5['data']
h5.close()


class ScikitVectorBacktester(object):
    ''' Class for the vectorized backtesting of
    Machine Learning-based trading strategies.

    Attributes
    ==========
    symbol: str
        Google Finance symbol with which to work
    start: str
        start date for data retrieval
    end: str
        end date for data retrieval
    amount: int, float
        amount to be invested at the beginning
    tc: float
        proportional transaction costs (e.g. 0.5% = 0.005) per trade
    model: str
        either 'regression' or 'logistic'

    Methods
    =======
    get_data:
        retrieves and prepares the base data set
    select_data:
        selects a sub-set of the data
    prepare_matrix:
        prepares the matrix for the model fitting
    fit_model:
        implements the fitting step
    run_strategy:
        runs the backtest for the regression-based strategy
    plot_results:
        plots the performance of the strategy compared to the symbol
    '''

    def __init__(self, symbol, start, end, amount, tc, model):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.amount = amount
        self.tc = tc
        self.results = None
        if model == 'regression':
            self.model = linear_model.LinearRegression()
        elif model == 'logistic':
            self.model = linear_model.LogisticRegression(C=1e6)
        else:
            raise ValueError('Model not known or not yet implemented.')
        self.get_data()

    def get_data(self):
        ''' Retrieves and prepares the data.
        '''
        try:
            raw = web.DataReader(self.symbol, data_source='google',
                             start=self.start, end=self.end)['Close']
            raw = pd.DataFrame(raw)
            raw.rename(columns={'Adj Close': 'price'}, inplace=True)
        except:
            raw = data[self.symbol]
            raw = raw[(raw.index > self.start) & (raw.index < self.end)]
            raw = pd.DataFrame(raw)
            raw.rename(columns={self.symbol: 'price'}, inplace=True)
        
        raw['returns'] = np.log(raw / raw.shift(1))
        self.data = raw.dropna()

    def select_data(self, start, end):
        ''' Selects sub-sets of the financial data.
        '''
        data = self.data[(self.data.index >= start) &
                         (self.data.index <= end)].copy()
        return data

    def prepare_matrix(self, start, end):
        ''' Prepares the matrix for the regression and prediction steps.
        '''
        data = self.select_data(start, end)
        matrix = np.zeros((self.lags + 1, len(data) - self.lags))
        for i in range(self.lags + 1):
            if i == self.lags:
                matrix[i] = data.returns.values[i:]
            else:
                matrix[i] = data.returns.values[i:i - self.lags]
        self.matrix = matrix

    def fit_model(self, start, end):
        ''' Implements the fitting step.
        '''
        self.prepare_matrix(start, end)
        self.model.fit(self.matrix[:self.lags].T,
                       np.sign(self.matrix[self.lags]))

    def run_strategy(self, start_in, end_in, start_out, end_out, lags=3):
        ''' Backtests the trading strategy.
        '''
        self.lags = lags
        self.fit_model(start_in, end_in)
        data = self.select_data(start_out, end_out)
        self.prepare_matrix(start_out, end_out)
        prediction = self.model.predict(self.matrix[:self.lags].T)
        data['prediction'] = 0.0
        data['prediction'].ix[self.lags:] = prediction
        data['strategy'] = data['prediction'] * data['returns']
        # determine when a trade takes place
        trades = data['prediction'].diff().fillna(0) != 0
        # subtract transaction costs from return when trade takes place
        data['strategy'][trades] -= self.tc
        data['creturns'] = self.amount * data['returns'].cumsum().apply(np.exp)
        data['cstrategy'] = self.amount * \
            data['strategy'].cumsum().apply(np.exp)
        self.results = data.ix[self.lags:]
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
    scibt = ScikitVectorBacktester('^GSPC', '2010-1-1', '2016-10-31',
                                   10000, 0.0, 'regression')
    print(scibt.run_strategy('2010-1-1', '2016-10-31',
                             '2010-1-1', '2016-10-31'))
    print(scibt.run_strategy('2010-1-1', '2014-12-31',
                             '2015-1-1', '2016-10-31'))
    scibt = ScikitVectorBacktester('^GSPC', '2010-1-1', '2016-10-31',
                                   10000, 0.0, 'logistic')
    print(scibt.run_strategy('2010-1-1', '2016-10-31',
                             '2010-1-1', '2016-10-31'))
    print(scibt.run_strategy('2010-1-1', '2014-12-31',
                             '2015-1-1', '2016-10-31'))
    scibt = ScikitVectorBacktester('^GSPC', '2010-1-1', '2016-10-31',
                                   10000, 0.001, 'logistic')
    print(scibt.run_strategy('2010-1-1', '2016-10-31',
                             '2010-1-1', '2016-10-31', lags=15))
    print(scibt.run_strategy('2010-1-1', '2014-12-31',
                             '2015-1-1', '2016-10-31', lags=15))
