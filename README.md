# moneyquant
moneyquant/
├── config/                # 配置文件
│   └── okx_api.py         # 欧易API密钥管理
├── data/                  # 数据模块
│   ├── okx_fetcher.py     # 欧易API数据获取
│   └── data_adapter.py    # 数据格式转换
├── strategies/            # 策略模块
│   └── ma_crossover.py    # 均线交叉策略
├── core/                  # 核心引擎
│   └── backtest_engine.py # 回测引擎封装
├── utils/                 # 工具模块
│   └── logger.py         # 日志管理
└── main.py                # 主程序入口
