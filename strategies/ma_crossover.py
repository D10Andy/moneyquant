import backtrader as bt

class MACrossover(bt.Strategy):
    params = (
        ('fast_period', 10),
        ('slow_period', 30),
    )

    def __init__(self):
        self.fast_ma = bt.indicators.SMA(self.data.close, period=self.p.fast_period)
        self.slow_ma = bt.indicators.SMA(self.data.close, period=self.p.slow_period)
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
        self.order = None  # 跟踪活跃订单

    def next(self):
        # 存在未完成订单时禁止新交易
        if self.order:
            return
        # 确保指标有效
        if len(self.data) < max(self.params.fast_period, self.params.slow_period):
            return
        
        print(f"[{self.data.datetime.date(0)}] Fast MA: {self.fast_ma[0]:.2f}, Slow MA: {self.slow_ma[0]:.2f}, Crossover: {self.crossover[0]}, Position: {self.position.size}")
        
        # 核心交易逻辑（必须保留buy/close调用）
        # if not self.position:
        if self.crossover[0] == 1 and self.crossover[-1] <= 0:
            # 金叉成立
            self.order = self.buy()  # 执行虚拟买入
            print(f'[{self.data.datetime.date(0)}] 虚拟买入信号触发')

        elif self.crossover[0] == -1 and self.crossover[-1] >= 0:
        # 死叉成立
            self.order = self.close()  # 执行虚拟平仓
            print(f'[{self.data.datetime.date(0)}] 虚拟卖出信号触发')

    def notify_order(self, order):
        """订单状态回调"""
        if order.status in [order.Submitted, order.Accepted]:
            # 订单已提交/接受（未成交）
            return

        if order.status == order.Completed:
            if order.isbuy():
                print(f'[买入成交] 价格: {order.executed.price}, 数量: {order.executed.size}')
            else:
                print(f'[卖出成交] 价格: {order.executed.price}, 数量: {order.executed.size}')
            # 重置订单引用
            self.order = None

        # 处理订单失败情况
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f'[订单异常] 状态: {order.getstatusname()}')
            self.order = None