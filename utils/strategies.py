import pandas as pd 
import os 
from tqdm import tqdm
import mplfinance as fplt
from glob import glob 
from utils.indicators import movingAverageConverganceDivergance as macdI
from utils.indicators import relativeStrengthIndex as rsiI
from utils.indicators import averageTrueRange as atrI
from utils.indicators import bollingerBands as bbI 
from utils.indicators import stochasticIndicator as stiI

from backtesting import Backtest, Strategy 
from backtesting.lib import crossover, barssince, SignalStrategy, TrailingStrategy


class BuyAndHoldStrategy(Strategy): 
    bb_window = 30 

    rsi_window = 14
    rsi_smooth_window = 3
    rsi_upper_thres = 70 
    rsi_lower_thres = 30 

    macd_fast_ma_length = 26 
    macd_slow_ma_length = 12
    macd_signal_ma_length = 9
    def init(self): 
        pass 

    def next(self): 
        if not self.position: 
            self.buy()


class MACDStrategy(Strategy): 
    bb_window = 30 

    rsi_window = 14
    rsi_smooth_window = 3
    rsi_upper_thres = 70 
    rsi_lower_thres = 30 

    macd_fast_ma_length = 26 
    macd_slow_ma_length = 12
    macd_signal_ma_length = 9

    def init(self): 
        stock_df = pd.DataFrame({ 
            "Open": self.data.Open, 
            "High": self.data.High, 
            "Low": self.data.Low, 
            "Close": self.data.Close, 
            "Volume": self.data.Volume
        })
        self.macd, self.macd_signal, self.hist = self.I(macdI, 
                        stock_df, 'EMA', 'EMA',
                        self.macd_fast_ma_length, 
                        self.macd_slow_ma_length, 
                        self.macd_signal_ma_length)

    def next(self):  
        if(crossover(self.macd, self.macd_signal) and self.macd[-1] <= 0): 
            if not self.position: 
                self.buy(size = 100)  
        elif(crossover(self.macd_signal, self.macd) and self.macd[-1] > 0): 
            if self.position: 
                self.position.close()



class BollingerBandsStrategy(Strategy): 
    bb_window = 30 

    rsi_window = 14
    rsi_smooth_window = 3
    rsi_upper_thres = 70 
    rsi_lower_thres = 30 

    macd_fast_ma_length = 26 
    macd_slow_ma_length = 12
    macd_signal_ma_length = 9

    def init(self): 
        stock_df = pd.DataFrame({ 
            "Open": self.data.Open, 
            "High": self.data.High, 
            "Low": self.data.Low, 
            "Close": self.data.Close, 
            "Volume": self.data.Volume
        })
        self.bb_basis, self.bb_upper, self.bb_lower = self.I(bbI, stock_df, self.bb_window)
        self.rsi, self.rsi_signal = self.I(rsiI, stock_df, self.rsi_window, self.rsi_smooth_window)
        
    def next(self): 
        close = self.data.Close 

        if(close[-1] < self.bb_lower[-1] and self.rsi_signal < self.rsi_lower_thres): 
            if not self.position: 
                self.buy(size = 100, sl = close[-1]*0.975)

        if(close[-1] > self.bb_upper[-1] and self.rsi_signal > self.rsi_upper_thres): 
            if self.position: 
                self.position.close


class SimpleMovingAverageStrategy(Strategy): 
    def init(self): 
        pass 

    def next(self): 
        pass 



