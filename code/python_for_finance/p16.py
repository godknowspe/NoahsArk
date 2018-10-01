# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 16:43:19 2017

@author: Gary
"""

import numpy as np
import pandas as pd
#import pandas.io.data as web
from pandas_datareader import data as web
import datetime

start = datetime.datetime(2014, 1, 2)
end = datetime.datetime(2016, 1, 6)
goog = web.DataReader('GOOG' , 'google' , start, end)
print(goog.tail())

goog['Log_Ret'] = np.log(goog['Close'] / goog['Close'].shift(1))
#OLD API
#goog['Volatility'] = pd.rolling_std(goog['Log_Ret'], window=252) * np.sqrt(252)
goog['Volatility'] = goog['Log_Ret'].rolling(window=252).std() * np.sqrt(252)
goog[['Close', 'Log_Ret', 'Volatility']].plot(subplots=True, color='blue', figsize=(8, 9))