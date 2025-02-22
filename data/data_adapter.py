import backtrader as bt

class BacktraderDataAdapter:
    @staticmethod
    def convert_to_btfeed(dataframe):
        # 添加openinterest列
        dataframe['openinterest'] = 0
        
        return bt.feeds.PandasData(
            dataname=dataframe,
            datetime=None,
            open=0,    # 修正列索引
            high=1,
            low=2,
            close=3,
            volume=4,
            openinterest=5
        )