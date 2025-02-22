# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import backtrader as bt
from config.okx_api import API_KEY, SECRET_KEY
from data.okx_fetcher import OkxFetcher
from data.data_adapter import BacktraderDataAdapter
from strategies.ma_crossover import MACrossover
from core.backtest_engine import BacktestEngine

# 初始化组件
fetcher = OkxFetcher(API_KEY, SECRET_KEY, is_proxies=True, http="127.0.0.1", port="7897")
engine = BacktestEngine()

# 获取数据
data_type = "local"
if data_type == "local":
    btc_data = pd.read_csv("./dataset/tmp_okx_btc_test.csv", index_col="datetime", parse_dates=True)
else:
    btc_data = fetcher.fetch_ohlcv('BTC/USDT', '1d', since=1704067200000)  # 2022年数据
    # btc_data.to_csv("./dataset/tmp_okx_btc_test.csv")
print(btc_data.head(2), btc_data.dtypes)
bt_feed = BacktraderDataAdapter.convert_to_btfeed(btc_data)
# 配置策略
# engine.cerebro.addstrategy(MACrossover)
engine.configure(strategy=MACrossover, init_cash=1000000, commission=0.001
            ,analyzers=[
            (bt.analyzers.TradeAnalyzer, {'_name': 'trades'}),
            (bt.analyzers.SharpeRatio, {'_name': 'sharpe'}),
            (bt.analyzers.DrawDown, {'_name': 'drawdown'})
            ]
        )

# 执行回测
result = engine.run_backtest(bt_feed)

# 输出结果
print(f'最终资产: {engine.cerebro.broker.getvalue():.2f}')
sharpe_data = result['analyzers']['sharpe'].get_analysis()
sharpe_ratio = sharpe_data.get('sharperatio', None)
print(f"夏普比率: {sharpe_ratio}")
# result['analyzers']['drawdown'].get_analysis().get('max', {}).get("drawdown", None)
print(f"最大回撤: {result['analyzers']['drawdown'].get_analysis().get('max', {}).get('drawdown', None)}%")
print(f"交易记录: {engine.get_trade_log(result['strategy'])}")
engine.cerebro.plot()
