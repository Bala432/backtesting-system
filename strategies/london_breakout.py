from .base import Strategy
from utils.indicators import Indicators

class LondonBreakoutStrategy(Strategy):
    def __init__(self, df, atr_window, atr_sl, entry_time):
        super().__init__(df)
        self.atr_window = atr_window
        self.atr_sl = atr_sl
        self.entry_time = entry_time
        
    def generate_signals(self):
        self.df['ATR'] = Indicators.get_ATR(self.df, self.atr_window)
        self.df = Indicators.add_day(self.df)
        self.df = Indicators.get_london_opening(self.df, self.entry_time)

        # Generate Signals
        for index in range(20, len(self.df)):
            london_opening = self.df['london_opening'].iloc[index]
            close_price = self.df['Close'].iloc[index]
            
            maximum_rolling = self.df['Close'].rolling(8).max().iloc[index]
            minimum_rolling = self.df['Close'].rolling(8).min().iloc[index]
            
            signal = 0
            if london_opening == True:
                if close_price >= maximum_rolling:
                    signal = 1
                elif close_price <= minimum_rolling:
                    signal = -1

            self.df.at[self.df.index[index], 'signal'] = signal
        return self.df