#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 16:10:43 2020

@author: bstaverosky
"""

import pandas as pd
print(pd.__version__)
pd.set_option("display.max_rows", None, "display.max_columns", None)
import yfinance as yf
import matplotlib.pyplot as plt
import talib as talib
import seaborn as sns
import statsmodels.api as sm
import numpy as np
import pyfolio as pf
import math

asset = "SPY"
asset = yf.download(asset, start='1900-01-01', progress=False)


# Calculate p2h signal

for i in range(len(asset.index)):
    if asset.loc[asset.index[i], "Close"]/np.max(asset.loc[asset.index[(i-252):(i-1)], "Close"]) > 0.9:
        asset.loc[asset.index[i], "p2h"] = 1
    else:
        asset.loc[asset.index[i], "p2h"] = 0

# TEST COMMENT FOR GIT COMMIT
# Calculate signal logic

asset['return'] = asset['Close'].pct_change()
asset['score'] = asset['p2h']
asset['signal'] = asset['score']
asset['signal'] = asset['signal'].shift(1)
asset['strat'] = np.nan

for i in range(len(asset.index)):
    if asset.loc[asset.index[i], "signal"] == 1:
        asset.loc[asset.index[i], "strat"] = asset.loc[asset.index[i], "return"]*3
    else:
        asset.loc[asset.index[i], "strat"] = 0
        
bmk_series = asset.loc[:,"return"]
strat_series = asset.loc[:,"strat"]
pf.create_simple_tear_sheet(returns = strat_series, benchmark_rets=bmk_series)
