#!/usr/bin/env python
# -*- coding: utf-8 -*-


from zipline.api import order_target, record, symbol
import matplotlib.pyplot as plt
from zipline.pipeline.factors import RSI


def initialize(context):
    context.i = 0
    context.asset = symbol('000001')


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return

    # Compute averages
    # data.history() has to be called with the same params
    # from above and returns a pandas dataframe.
    ma100 = data.history(context.asset, 'price', bar_count=100, frequency="1d").mean()
    ma300 = data.history(context.asset, 'price', bar_count=300, frequency="1d").mean()

    # Trading logic
    if ma100 > ma300:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target(context.asset, 100)
    elif ma100 < ma300:
        order_target(context.asset, 0)

    # Save values for later inspection
    record(mydata=data.current(context.asset, 'price'),
           ma100=ma100,
           ma300=ma300)


def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')

    ax2 = fig.add_subplot(212)
    perf['mydata'].plot(ax=ax2)
    perf[['ma100', 'ma300']].plot(ax=ax2)

    perf_trans = perf.ix[[t != [] for t in perf.transactions]]
    buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.ix[
        [t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax2.plot(buys.index, perf.ma100.ix[buys.index],
             '^', markersize=10, color='m')
    ax2.plot(sells.index, perf.ma300.ix[sells.index],
             'v', markersize=10, color='k')
    ax2.set_ylabel('Price in rmb')
    plt.legend(loc=0)
    plt.show()
