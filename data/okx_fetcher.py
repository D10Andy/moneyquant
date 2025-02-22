import ccxt
import pandas as pd
from datetime import datetime

class OkxFetcher:
    def __init__(self, api_key, secret, is_proxies=False, http="127.0.0.1", port="7897"):
        okx_params = {
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True
        }
        if is_proxies:
            okx_params["proxies"] = {'http': f'{http}:{port}', 'https': f'{http}:{port}'}
        self.exchange = ccxt.okx(okx_params)

    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=100000):
        """获取欧易历史K线数据"""
        data = self.exchange.fetch_ohlcv(
            symbol, 
            timeframe=timeframe,
            since=since,
            limit=limit
        )
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df[['datetime', 'open', 'high', 'low', 'close', 'volume']].set_index('datetime')


if __name__ == "__main__":
    import time
    from datetime import datetime, timedelta
    
    # 初始化获取器
    fetcher = OkxFetcher("", "", is_proxies=True, http="127.0.0.1", port="7897")
    
    # 时间范围设置
    start_date = datetime(2020, 1, 1, 0, 0, 0)
    end_date = datetime(2025, 1, 1, 0, 0, 0)
    current_since = int(start_date.timestamp() * 1000)  # 转换为毫秒时间戳 
    end_timestamp = int(end_date.timestamp() * 1000)
    
    # 初始化DataFrame
    all_data = pd.DataFrame()
    
    # 分批次获取逻辑
    batch_size = 100  # 每次获取条数
    while current_since < end_timestamp:
        try:
            # 获取数据（limit参数实际受交易所API限制，需根据实际情况调整）
            df = fetcher.fetch_ohlcv('BTC/USDT', '1h', since=current_since, limit=batch_size)
            
            # 过滤超出结束时间的数据
            df = df[df.index <= pd.to_datetime(end_timestamp, unit='ms')]
            if df.empty:
                break
                
            # 增量合并数据 
            all_data = pd.concat([all_data, df]).drop_duplicates()
            
            # 更新下一个批次起始时间（取最后时间+1小时）
            last_timestamp = df.index[-1].value // 10**6  # 将ns转换为ms
            current_since = last_timestamp + 3600000  # 增加1小时
            
            # 进度显示
            print(f"已获取至 {df.index[-1].strftime('%Y-%m-%d %H:%M')} 数据, {last_timestamp}, {current_since}")
            
            # API速率限制规避 
            time.sleep(1)  
            
        except Exception as e:
            print(f"获取数据异常: {str(e)}")
            time.sleep(5)
    
    # 保存结果
    all_data.to_csv('../dataset/btc_ohlcv_2020-2025.csv')
    print(f"数据已保存，总条数：{len(all_data)}")
