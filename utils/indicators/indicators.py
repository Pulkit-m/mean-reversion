import pandas as pd 

def movingAverageConverganceDivergance(stock_df, smooth_source = 'EMA', smooth_signal = 'EMA', fast_ma = 12, slow_ma = 26, signal_ma = 9): 
    """
        Calculate Moving Average Convergence Divergence (MACD) and related indicators.

        Parameters:
        - stock_df (DataFrame): Pandas containing stock data with 'close' prices.
        - smooth_source (str): Type of smoothing for source data. Default is 'EMA' (Exponential Moving Average).
        - smooth_signal (str): Type of smoothing for signal data. Default is 'EMA' (Exponential Moving Average).
        - fast_ma (int): Time period for the fast moving average. Default is 12.
        - slow_ma (int): Time period for the slow moving average. Default is 26.
        - signal_ma (int): Time period for the signal line moving average. Default is 9.

        Returns:
        - macd (Series): MACD line.
        - signal (Series): Signal line.
        - hist (Series): MACD histogram.
    """
    fast_src = stock_df.close.ewm(span = fast_ma, adjust=False).mean() if smooth_source == 'EMA' else stock_df.close.rolling(fast_ma).mean()  
    slow_src = stock_df.close.ewm(span = slow_ma, adjust=False).mean() if smooth_source == 'EMA' else stock_df.close.rolling(slow_ma).mean()

    macd = fast_src - slow_src 
    signal = macd.ewm(span = signal_ma, adjust=False).mean() if smooth_signal == 'EMA' else macd.rolling(signal_ma).mean()

    hist = macd - signal 

    return (macd, signal, hist)



def bollingerBands(stock_df, ma_window): 
    """
    Calculate Bollinger Bands for a given stock DataFrame.

    Bollinger Bands consist of a middle band (simple moving average) and two outer bands 
    (standard deviations above and below the middle band) that help identify price volatility and potential 
    reversal points.

    Parameters:
    - stock_df (DataFrame): A pandas DataFrame containing stock data, with at least 'close' prices.
    - ma_window (int): The window size for the moving average calculation.

    Returns:
    - tuple: A tuple containing:
        - basis_ma (Series): The middle band, calculated as the simple moving average of 'close' prices.
        - (upper_band, lower_band) (tuple of Series): The upper and lower Bollinger Bands, calculated as 
          deviations from the middle band.
    """
    basis_ma = stock_df.close.rolling(ma_window).mean() 
    deviation = stock_df.close.rolling(ma_window).std() 

    upper_band = basis_ma + deviation 
    lower_band = basis_ma - deviation 
    
    return (basis_ma, (upper_band, lower_band))