from .base import Strategy
from utils.indicators import Indicators

class BollingerBandStrategy(Strategy):
    def __init__(self, df, fast_window, slow_window, atr_window, atr_sl, bollinger_window, std_multiplier):
        super().__init__(df)
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.atr_window = atr_window
        self.atr_sl = atr_sl
        self.bollinger_window = bollinger_window
        self.std_multiplier = std_multiplier
        
    def generate_signals(self):
        self.df = Indicators.get_sma(self.df, self.fast_window, self.slow_window)
        self.df['ATR'] = Indicators.get_ATR(self.df, self.atr_window)
        self.df = Indicators.get_bollinger_bands(self.df, self.bollinger_window, self.std_multiplier)

        # Generate Signals
        for index in range(200, len(self.df)):
            previous_fast_sma = self.df['fast_sma'].iloc[index-1]
            previous_slow_sma = self.df['slow_sma'].iloc[index-1]
            
            close_price = self.df['Close'].iloc[index]
            rolling_mean = self.df['rolling_mean'].iloc[index]
            last_close_prices = self.df['Close'].iloc[index-4 : index].values
            last_lower_band_prices = self.df['lower_band'].iloc[index-4 : index].values
            last_upper_band_prices = self.df['upper_band'].iloc[index-4 : index].values
            
            if previous_fast_sma > previous_slow_sma and close_price >= rolling_mean \
                and any(last_close_prices <= last_lower_band_prices):
                self.df.at[self.df.index[index], 'signal'] = 1
            elif previous_fast_sma < previous_slow_sma and close_price <= rolling_mean \
                and any(last_close_prices >= last_upper_band_prices):
                self.df.at[self.df.index[index], 'signal'] = -1
            else:
                self.df.at[self.df.index[index], 'signal'] = 0
                
        return self.df