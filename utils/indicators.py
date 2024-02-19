import pandas as pd 

def movingAverageConverganceDivergance(stock_df, source_ma_type = 'EMA', 
                                       signal_ma_type = 'EMA', fast_ma_length = 12,
                                        slow_ma_length = 26, signal_ma_length = 9): 
    """
        Calculate Moving Average Convergence Divergence (MACD) and related indicators.

        Parameters:
        - stock_df (DataFrame): Pandas containing stock data with 'Close' prices.
        - source_ma_type (str): Type of smoothing for source data. Default is 'EMA' (Exponential Moving Average).
        - signal_ma_type (str): Type of smoothing for signal data. Default is 'EMA' (Exponential Moving Average).
        - fast_ma_length (int): Time period for the fast moving average. Default is 12.
        - slow_ma_length (int): Time period for the slow moving average. Default is 26.
        - signal_ma_length (int): Time period for the signal line moving average. Default is 9.

        Returns:
        - macd (Series): MACD line.
        - signal (Series): Signal line.
        - hist (Series): MACD histogram.
    """
    fast_src = stock_df.Close.ewm(span = fast_ma_length, adjust=False).mean() if source_ma_type == 'EMA' else stock_df.Close.rolling(fast_ma_length).mean()  
    slow_src = stock_df.Close.ewm(span = slow_ma_length, adjust=False).mean() if source_ma_type == 'EMA' else stock_df.Close.rolling(slow_ma_length).mean()

    macd = fast_src - slow_src 
    signal = macd.ewm(span = signal_ma_length, adjust=False).mean() if signal_ma_type == 'EMA' else macd.rolling(signal_ma_length).mean()

    hist = macd - signal 

    return pd.DataFrame({
        "macd": macd, 
        "macd_signal": signal, 
        "macd_hist": hist
    })
    # return (macd, signal, hist)


def bollingerBands(stock_df, ma_window = 20): 
    """
    Calculate Bollinger Bands for a given stock DataFrame.

    Bollinger Bands consist of a middle band (simple moving average) and two outer bands 
    (standard deviations above and below the middle band) that help identify price volatility and potential 
    reversal points.

    Parameters:
    - stock_df (DataFrame): A pandas DataFrame containing stock data, with at least 'Close' prices.
    - ma_window (int): The window size for the moving average calculation. default value is 20.

    Returns:
    - tuple: A tuple containing:
        - basis_ma (Series): The middle band, calculated as the simple moving average of 'Close' prices.
        - (upper_band, lower_band) (tuple of Series): The upper and lower Bollinger Bands, calculated as 
          deviations from the middle band.
    """
    basis_ma = stock_df.Close.rolling(ma_window).mean() 
    deviation = stock_df.Close.rolling(ma_window).std() 

    upper_band = basis_ma + 2*deviation 
    lower_band = basis_ma - 2*deviation 
    return pd.DataFrame({
        "bb_basis": basis_ma, 
        "bb_upper": upper_band,     
        "bb_lower": lower_band
    })
    # return (basis_ma, (upper_band, lower_band)) 


def relativeStrengthIndex(stock_df, rsi_window = 14, ma_length = 14, smooth_signal = 'EMA'): 
    """
    Calculates the Relative Strength Index (RSI) of a given stock DataFrame.

    Parameters:
    - stock_df (DataFrame): DataFrame containing stock data with at least a 'Close' column.
    - rsi_window (int): Window size for computing the average gain and average loss.
    - ma_length (int): Length of the moving average used for smoothing the RSI.
    - smooth_signal (str): Smoothing technique for the RSI. Options: 'EMA' (Exponential Moving Average)
                           or 'SMA' (Simple Moving Average). Default is 'EMA'.

    Returns:
    - rsi (Series): Series containing the computed RSI values.
    - rsi_smooth (Series): Series containing the smoothed RSI values based on the chosen smoothing technique.
    """

    delta = stock_df.Close.diff() 
    gains = delta.where(delta>0,0) 
    losses = -delta.where(delta<0,0)

    avg_gain = gains.ewm(span=rsi_window).mean() 
    avg_loss = losses.ewm(span=rsi_window).mean()

    rs = avg_gain/avg_loss  
    rsi = 100 - (100/(1+rs)) 
    rsi_smooth = rsi.ewm(span = ma_length).mean() if smooth_signal == 'EMA' else rsi.rolling(ma_length).mean() 

    return pd.DataFrame({
        "rsi": rsi, 
        "rsi_signal": rsi_smooth
    })
    # return (rsi, rsi_smooth)


def stochasticIndicator(stock_df, k_period = 14, d_period = 3): 
    """
    Calculates the Stochastic Oscillator indicator for a given stock DataFrame.

    The Stochastic Oscillator is a momentum indicator comparing a particular closing price of a security to a range of its prices over a certain period of time. The indicator's formula is as follows:

    %K = 100 * (Close - Lowest Low) / (Highest High - Lowest Low)

    Where:
    - Close represents the closing price of the stock.
    - Lowest Low represents the lowest price traded during the given period.
    - Highest High represents the highest price traded during the given period.

    This function computes both the %K and a smoothed version of %K using the provided periods.

    Parameters:
    - stock_df (DataFrame): DataFrame containing stock data with columns ['high', 'low', 'Close'].
    - k_period (int, optional): The lookback period for calculating the highest high and lowest low. Default is 14.
    - d_period (int, optional): The smoothing period for the %K line. Default is 3.

    Returns:
    - tuple: A tuple containing two pandas Series objects representing the %K line and the smoothed %K line, respectively.
    """
    k_period = 14 
    d_period = 3 

    high_rolling = stock_df.High.rolling(k_period).max() 
    low_rolling = stock_df.Low.rolling(k_period).min() 
    percent_k = 100 * (stock_df.Close - low_rolling)/(high_rolling - low_rolling)  

    smooth_k = percent_k.rolling(d_period).mean() 
    return pd.DataFrame({
        "stoch": percent_k, 
        "stoch_smooth": smooth_k
    })
    # return (percent_k, smooth_k)


def averageTrueRange(stock_df, period = 14) -> pd.Series: 
    """
    Calculate the Average True Range (ATR) of a stock.

    ATR is a technical analysis indicator that measures market volatility by decomposing 
    the entire range of an asset price for that period. It considers the true range, 
    which is the maximum of the current high less the current low, current high less 
    the previous Close, or the current low less the previous Close, and then averages 
    this value over a specified period.

    Parameters:
        stock_df (pd.DataFrame): DataFrame containing stock data with columns: 'high', 'low', 'Close'.
        period (int): The number of periods to consider for calculating the ATR. Default is 14.

    Returns:
        pd.Series: A Series containing the Average True Range values.
    """
    high = stock_df.High 
    low = stock_df.Low 
    Close = stock_df.Close 

    todays_range = abs(high - low) 
    todays_high_vs_yesterdays_close = abs(high - Close.shift()) 
    todays_low_vs_yesterdays_close = abs(low - Close.shift()) 

    tr = pd.concat([todays_range, todays_high_vs_yesterdays_close, todays_low_vs_yesterdays_close], axis = 1).max(axis = 1)
    atr = tr.ewm(alpha = 1/period).mean() # this is rma 

    return pd.DataFrame({
        "atr": atr
    })
    # return atr 