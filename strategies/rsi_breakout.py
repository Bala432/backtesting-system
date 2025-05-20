from .base import Strategy
from utils.indicators import Indicators

class RSIBreakoutStrategy(Strategy):
    def __init__(self, df, atr_window, atr_sl, rsi_window, average_window, overbought, oversold):
        super().__init__(df)
        self.atr_window = atr_window
        self.atr_sl = atr_sl
        self.rsi_window = rsi_window
        self.average_window = average_window
        self.overbought = overbought
        self.oversold = oversold
        
    def generate_signals(self):
        self.df['ATR'] = Indicators.get_ATR(self.df, self.atr_window)
        self.df = Indicators.get_rsi(self.df, self.rsi_window)
        self.df = Indicators.get_average_close_price(self.df, self.average_window)
        
        for index in range(20, len(self.df)):
            previous_close_price = self.df['Close'].iloc[index-1]
            previous_average_close_price = self.df['average_close'].iloc[index-1]
            
            current_close_price = self.df['Close'].iloc[index]
            current_average_close_price = self.df['average_close'].iloc[index]
            
            rsi = self.df['RSI'].iloc[index]
            signal = 0
            
            # Generate Signals
            if rsi < self.oversold and previous_close_price < previous_average_close_price \
                and current_close_price >= current_average_close_price:
                    signal = 1
            elif rsi > self.overbought and previous_close_price > previous_average_close_price \
                and current_close_price <= current_average_close_price:
                    signal = -1
                    
            self.df.at[self.df.index[index], 'signal'] = signal
            
        return self.df