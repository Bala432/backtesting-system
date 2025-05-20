from .base import Strategy
from utils.indicators import Indicators
import pandas as pd

class MovingAverageStrategy(Strategy):
    def __init__(self, df, fast_window, slow_window, atr_window, atr_sl):
        super().__init__(df)
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.atr_window = atr_window
        self.atr_sl = atr_sl
        
    def generate_signals(self):
        self.df = Indicators.get_sma(self.df, self.fast_window, self.slow_window)
        self.df['ATR'] = Indicators.get_ATR(self.df, self.atr_window)
    
        # Generate Entry Signals
        for index in range(1, len(self.df)):
            previous_fast_sma = self.df['fast_sma'].iloc[index-1]
            previous_slow_sma = self.df['slow_sma'].iloc[index-1]
            
            current_fast_sma = self.df['fast_sma'].iloc[index]
            current_slow_sma = self.df['slow_sma'].iloc[index]
            
            if pd.isna(previous_fast_sma) or pd.isna(previous_slow_sma) \
                or pd.isna(current_fast_sma) or pd.isna(current_slow_sma):
                continue
                    
            if previous_fast_sma < previous_slow_sma and current_fast_sma >= current_slow_sma:
                self.df.at[self.df.index[index], 'signal'] = 1
            elif previous_fast_sma < previous_slow_sma and current_fast_sma >= current_slow_sma:
                self.df.at[self.df.index[index], 'signal'] = -1
    
        return self.df