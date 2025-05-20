import pandas as pd

class DataLoader:
    @staticmethod
    def load_csv(path):
        df = pd.read_csv(path)
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Date'] = df['Date'].str.split(' ').str[0:2]
        df['Date'] = df['Date'].str.join(' ')
        df.set_index('Date', inplace = True)
        df.index = pd.to_datetime(df.index, format = '%d.%m.%Y %H:%M:%S.%f')
        return df