import numpy as np

# Calculate the Compound Annual Growth Rate (CAGR) of a strategy
def CAGR(df, initial_balance, period_per_year=252*24):
    df = df.copy()
    number_of_years = len(df) / period_per_year
    cumulative_sum = df['cumulative_sum'].iloc[-1]
    if number_of_years <= 0 or initial_balance <= 0:
        return np.nan
    cagr = (cumulative_sum / initial_balance) ** (1 / number_of_years) - 1
    return round(cagr * 100, 2)

# Calculate the Sharpe Ratio of the strategy.
def sharpe_ratio(df, risk_free_rate=0.02, period_per_year=252):
    df = df.copy()
    returns = df['cumulative_sum'].pct_change().dropna()
    mean_return = returns.mean() * period_per_year
    std_return = returns.std() * np.sqrt(period_per_year)
    excess_return = mean_return - risk_free_rate
    sharpe = excess_return / std_return if std_return != 0 else np.nan
    return round(sharpe, 2)

# Calculate the maximum drawdown of the strategy.
def max_drawdown(df):
    df = df.copy()
    cumulative_sum = df['cumulative_sum']
    running_max = cumulative_sum.cummax()
    drawdown = 1 - cumulative_sum / running_max
    max_drawdown = drawdown.max()
    return round(max_drawdown * 100, 2)

# Calculate win rate from trade log DataFrame.
def win_rate(trade_log):
    if trade_log.empty:
        return 0.0
    wins = trade_log[trade_log['Net PnL'] > 0].shape[0]
    total = trade_log.shape[0]
    return round(100 * wins / total, 2)

# Calculate profit factor from trade log DataFrame.
def profit_factor(trade_log):
    if trade_log.empty:
        return np.nan
    gross_profit = trade_log[trade_log['Net PnL'] > 0]['Net PnL'].sum()
    gross_loss = trade_log[trade_log['Net PnL'] < 0]['Net PnL'].sum()
    if gross_loss == 0:
        return np.nan
    return round(gross_profit / abs(gross_loss), 2)