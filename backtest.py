from utils.data_loader import DataLoader
from strategies.moving_average import MovingAverageStrategy
from strategies.inside_bar import InsideBarStrategy
from strategies.bollinger_bands import BollingerBandStrategy
from strategies.london_breakout import LondonBreakoutStrategy
from strategies.rsi_breakout import RSIBreakoutStrategy
from engine.backtester import Backtester

def run():
    
    df = DataLoader.load_csv("data/EURUSD.csv")
    
    strategy = MovingAverageStrategy(df, 50, 200, 20, 0.5)
    
    #strategy = InsideBarStrategy(df, 50, 200, 20, 0.5)
    
    #strategy = BollingerBandStrategy(df, 50, 200, 20, 0.5, 50, 3)
    
    #strategy = LondonBreakoutStrategy(df, 20, 0.5, 8)
    
    #strategy = RSIBreakoutStrategy(df, 20, 0.5, 14, 5, 70, 30)
    
        
    df_signals = strategy.generate_signals()
    
    backtester = Backtester(df_signals)
    backtester.run()
    summary = backtester.summary()
    if summary == None:
        print("========== No Trade Execution Happened ===================")
    else:
        for key, value in summary.items():
            print(f'{key} : {value}')

if __name__ == '__main__':
    run()