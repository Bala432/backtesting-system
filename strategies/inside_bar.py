from .base import Strategy
from utils.indicators import Indicators

class InsideBarStrategy(Strategy):
    def __init__(self, df, fast_window, slow_window, atr_window, atr_sl):
        super().__init__(df)
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.atr_window = atr_window
        self.atr_sl = atr_sl
        
    def generate_signals(self):
        self.df = Indicators.get_sma(self.df, self.fast_window, self.slow_window)
        self.df['ATR'] = Indicators.get_ATR(self.df, self.atr_window)
        self.df = Indicators.get_inside_bar(self.df)
        
        for index in range(200,len(self.df)):
            previous_fast_sma = self.df['fast_sma'].iloc[index-1]
            previous_slow_sma = self.df['slow_sma'].iloc[index-1]
            close_price = self.df['Close'].iloc[index]
            open_price = self.df['Open'].iloc[index]

            inside_bar_1 = self.df['inside_bar'].iloc[index-1]
            inside_bar_2 = self.df['inside_bar'].iloc[index-2]
            inside_bar_3 = self.df['inside_bar'].iloc[index-3]

            # Buy/Sell Positions
            if inside_bar_1 and inside_bar_2 and inside_bar_3:
                if previous_fast_sma >= previous_slow_sma and close_price >= open_price:
                    self.df.at[self.df.index[index], 'signal'] = 1
                elif previous_fast_sma <= previous_slow_sma and close_price <= open_price:
                    self.df.at[self.df.index[index], 'signal'] = -1

        return self.df