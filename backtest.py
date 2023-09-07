from backtesting import Backtest, Strategy
import talib as ta
import pandas as pd
import datetime as dt
import os

data = pd.DataFrame(pd.read_excel(os.environ.get('EXCEL_SPXMIB_DATA')))
data.columns = ['Date', 'Close', 'Open', 'High', 'Low']

data.set_index('Date', inplace=True)

print(data)

class MomentumStrategy(Strategy):
    def init(self):
        self.macd_valid = False
        self.rsi_valid = False
        self.cci_valid = False

    def next(self):
        close_series = pd.Series(self.data['Close'])
        high_series = pd.Series(self.data['High'])
        low_series = pd.Series(self.data['Low'])

        macd, signal, _ = ta.MACD(close_series, fastperiod=12, slowperiod=26, signalperiod=9)

        if macd.iloc[-1] > 0 and macd.iloc[-1] > macd.iloc[-2]:
            self.macd_valid = True
        else:
            self.macd_valid = False

        rsi = ta.RSI(close_series, timeperiod=14)

        if rsi.iloc[-1] > 50:
            self.rsi_valid = True
        else:
            self.rsi_valid = False

        cci = ta.CCI(high_series, low_series, close_series, timeperiod=20)

        if cci.iloc[-2] > 0:
            self.cci_valid = True
        else:
            self.cci_valid = False

        # Entry and exit logic
        if self.macd_valid and self.rsi_valid and self.cci_valid:
            self.buy()
        elif self.position and (not self.macd_valid or not self.rsi_valid or not self.cci_valid):
            self.position.close()

bt = Backtest(data=data, strategy=MomentumStrategy, cash=2500,)
stats = bt.run()

print(stats)

bt.plot()