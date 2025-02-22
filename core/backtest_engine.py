import backtrader as bt

class BacktestEngine:
    def __init__(self):
        self._reset_cerebro()
        
    def _reset_cerebro(self):
        """重置回测引擎"""
        self.cerebro = bt.Cerebro()
        self.strategy = None  # 当前策略类
    
    def configure(self, 
                 strategy,    # 必须传入策略类
                 init_cash=100000, 
                 commission=0.001,
                 analyzers=None):
        """配置回测参数"""
        self._reset_cerebro()
        
        # 添加策略
        self.strategy = strategy
        self.cerebro.addstrategy(strategy)
        
        # 资金配置
        self.cerebro.broker.setcash(init_cash)
        self.cerebro.broker.setcommission(commission=commission)
        
        # 添加分析器
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        if analyzers:
            for analyzer in analyzers:
                # 正确解包 (类, 参数字典)
                self.cerebro.addanalyzer(analyzer[0], **analyzer[1]) 

    def run_backtest(self, data):
        """执行回测"""
        # 清除旧数据
        self.cerebro.data = []
        # 添加新数据
        # datafeed = bt.feeds.PandasData(dataname=data)
        self.cerebro.adddata(data)
        
        # 运行回测
        results = self.cerebro.run()
        
        # 返回策略实例和分析结果
        strat_instance = results[0]
        return {
            'strategy': strat_instance,
            'analyzers': {
                'sharpe': strat_instance.analyzers.getbyname('sharpe'),
                'drawdown': strat_instance.analyzers.getbyname('drawdown'),
                'returns': self.cerebro.broker.get_value()  # 最终资金
            }
        }

    def get_trade_log(self, strat_instance):
        """获取交易记录"""
        return strat_instance.analyzers.trades.get_analysis()