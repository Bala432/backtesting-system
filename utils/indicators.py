import pandas as pd

class Indicators:
    @staticmethod
    def get_sma(df, fast_window, slow_window):
        df['fast_sma'] = df['Close'].rolling(fast_window).mean()
        df['slow_sma'] = df['Close'].rolling(slow_window).mean()
        return df
    
    @staticmethod
    def get_ATR(df, ATR_window):
        high_low = abs(df['High'] - df['Low'])
        high_prev_close = abs(df['High'] - df['Close'].shift(1))
        low_prev_close = abs(df['Low'] - df['Close'].shift(1))
        tr = pd.concat([high_low, high_prev_close, low_prev_close], axis = 1).max(axis = 1)
        atr = tr.rolling(ATR_window).mean()
        return atr
    
    @staticmethod
    def get_inside_bar(df):
        current_high = df['High']
        current_low = df['Low']
        previous_high = df['High'].shift(1)
        previous_low = df['Low'].shift(1)

        df['inside_bar'] = ( current_high < previous_high ) & ( current_low > previous_low )
        return df
    
    @staticmethod
    def get_bollinger_bands(df, bollinger_window, std_multiplier):
        df['rolling_mean'] = df['Close'].rolling(bollinger_window).mean()
        df['rolling_std'] = df['Close'].rolling(bollinger_window).std()
        df['upper_band'] = df['rolling_mean'] + df['rolling_std'] * std_multiplier
        df['lower_band'] = df['rolling_mean'] - df['rolling_std'] * std_multiplier
        return df
    
    @staticmethod
    def add_day(df):
        df['Day'] = df.index.dayofweek
        dmap = {0 : 'Mon', 1 : 'Tue', 2 : 'Wed', 3 : 'Thu', 4 : 'Fri', 5 : 'Sat', 6 : 'Sun'}
        df['Day'] = df['Day'].map(dmap)
        return df
    
    @staticmethod
    def get_london_opening(df, entry_time):
        df['london_opening'] = df['Day'].index.hour == entry_time
        return df
    
    @staticmethod
    def get_rsi(df, rsi_window):
        df['Diff'] = df['Close'].diff(1)
        df['gains'] = df[df['Diff'] > 0]['Diff']
        df['losses'] = df[df['Diff'] < 0]['Diff']
        df['average_gains'] = df['gains'].rolling(rsi_window, min_periods = 1).mean()
        df['average_losses'] = df['losses'].rolling(rsi_window, min_periods = 1).mean()
        df['RS'] = abs( df['average_gains'] / df['average_losses'])
        df['RSI'] = 100 - ( 100 /( 1 + df['RS']))
        df.drop(['Diff','gains','losses', 'average_gains', 'average_losses', 'RS' ], axis = 1)
        return df
    
    @staticmethod
    def get_average_close_price(df, average_window):
        df['average_close'] = df['Close'].rolling(average_window).mean()
        return df