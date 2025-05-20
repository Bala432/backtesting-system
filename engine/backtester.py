import pandas as pd
from utils.metrics import CAGR, sharpe_ratio, max_drawdown, win_rate, profit_factor


class Trade:
    def __init__(self, entry_index, entry_price, exit_price, exit_index, direction, spread, size, take_profit, stop_loss, net_pnl):
        self.entry_price = entry_price
        self.entry_index = entry_index
        self.exit_price = None
        self.exit_index = None
        self.direction = direction
        self.spread = spread
        self.size = size
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.net_pnl = None
        
    def close(self, index, close_price):
        self.exit_index = index
        self.exit_price = close_price
        if self.direction == 'Buy':
            raw_pnl = ( self.exit_price - self.entry_price) * self.size
        else:
            raw_pnl = ( self.entry_price - self.exit_price ) * self.size
        spread_cost = self.spread * self.size
        self.net_pnl = raw_pnl - spread_cost
        
    def exit_type(self):
        if self.net_pnl is None:
            return None
        elif self.net_pnl > 0.1:
            return 'Profit'
        elif self.net_pnl < -0.1:
            return 'Loss'
        else:
            return 'Breakeven'

class Backtester:
    def __init__(self, df, account_size = 100000, size = 1, atr_sl = 0.5, slippage = 2):
        self.df = df
        self.account_size = account_size
        self.size = size * 10000
        self.atr_sl = atr_sl
        self.slippage = float(slippage) / 10000
        self.trades = []
    
    def run(self):
        open_trade = None
        for index in range(20, len(self.df)):
            row = self.df.iloc[index]
            row_index = self.df.index[index]
            
            atr = row['ATR'] * self.atr_sl
            signal = row['signal']
            close_price = row['Close']
            spread = self.slippage
            
            # Buy/Sell Positions
            if open_trade == None and signal == 1:
                take_profit = close_price + atr
                stop_loss = close_price - atr
                open_trade = Trade(row_index, close_price, None, None, 'Buy', spread, self.size, take_profit, stop_loss, None)
            elif open_trade == None and signal == -1:
                take_profit = close_price - atr
                stop_loss = close_price + atr
                open_trade = Trade(row_index, close_price, None, None, 'Sell', spread, self.size, take_profit, stop_loss, None)
                
            # Buy/Sell Profit/Loss
            if open_trade is not None:
                if open_trade.direction == 'Buy':
                    if close_price >= open_trade.take_profit:
                        open_trade.close(row_index, close_price)
                        self.trades.append(open_trade)
                        open_trade = None
                    elif close_price <= open_trade.stop_loss:
                        open_trade.close(row_index, close_price)
                        self.trades.append(open_trade)
                        open_trade = None
                elif open_trade.direction == 'Sell':
                    if close_price <= open_trade.take_profit:
                        open_trade.close(row_index, close_price)
                        self.trades.append(open_trade)
                        open_trade = None
                    elif close_price >= open_trade.stop_loss:
                        open_trade.close(row_index, close_price)
                        self.trades.append(open_trade)
                        open_trade = None
                        
        if open_trade is not None and open_trade.exit_price == None:
            last_price = self.df.iloc[index-1]['Close']
            open_trade.close(self.df.index[-1], last_price)
            self.trades.append(open_trade)   
            
    def get_trade_log(self):
        log = [{
            'Entry Time ' : t.entry_index,
            'Entry Price ' : t.entry_price,
            'Exit Time ' : t.exit_index,
            'Exit Price ' : t.exit_price,
            'Size ' : t.size,
            'Spread ' : t.size,
            'Direction ' : t.direction,
            'Take Profit ' : t.take_profit,
            'Stop Loss ' : t.stop_loss,
            'Net PnL' : t.net_pnl,
            'Exit Type ' : t.exit_type()
        } for t in self.trades]    
        return pd.DataFrame(log)    
            
    def summary(self):
        df = self.get_trade_log()
        df['cumulative_sum'] = df['Net PnL'].cumsum() + self.account_size

        if df.empty:
            return None
        print(df.head(5))
        profits = df[df['Net PnL'] > 0.1]['Net PnL']
        losses = df[df['Net PnL'] < -0.1]['Net PnL']
        breakevens = df[(df['Net PnL'] <= 0.1) & (df['Net PnL'] >= -0.1)]['Net PnL']
        
        metrics = {
                    'CAGR (%)': CAGR(df, self.account_size),
                    'Sharpe Ratio': sharpe_ratio(df),
                    'Max Drawdown (%)': max_drawdown(df),
                    'Win Rate (%)': win_rate(df),
                    'Profit Factor': profit_factor(df)
                }
        
        summary = {
            'Total Trades': len(df),
            'Profitable Trades': len(profits),
            'Loss Trades': len(losses),
            'Breakeven Trades': len(breakevens),
            'Max Profit Trade': profits.max() if not profits.empty else 0,
            'Max Loss Trade': losses.min() if not losses.empty else 0,
            'Win Rate (%)': 100 * len(profits) / len(df) if len(df) > 0 else 0,
            'Net PnL': df['Net PnL'].sum(),
            **metrics
        }
        return summary        