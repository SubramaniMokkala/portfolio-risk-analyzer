# Data Collection from yfinance package

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(ticker_symbol, start_date, end_date):
    """
    Fetch historical stock data for a given ticker symbol
    
    Args:
        ticker_symbol (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        start_date (datetime): Start date for historical data
        end_date (datetime): End date for historical data
    
    Returns:
        pandas.DataFrame: Historical stock data with columns:
                         Open, High, Low, Close, Volume, Dividends, Stock Splits
        None: If data fetch fails
    
    Example:
        >>> data = get_stock_data('AAPL', datetime(2024, 1, 1), datetime(2024, 12, 1))
        >>> print(data.head())
    """
    try:
        # Create ticker object
        ticker = yf.Ticker(ticker_symbol)
        
        # Fetch historical data
        # interval='1d' means daily data
        data = ticker.history(start=start_date, end=end_date, interval='1d')
        
        # Check if data is empty
        if data.empty:
            return None
        
        return data
    
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {str(e)}")
        return None


def get_stock_info(ticker_symbol):
    """
    Get company information for a stock ticker
    
    Args:
        ticker_symbol (str): Stock ticker symbol
    
    Returns:
        dict: Company information including name, sector, market cap, etc.
        None: If fetch fails
    
    Example:
        >>> info = get_stock_info('AAPL')
        >>> print(info['longName'])  # 'Apple Inc.'
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        return info
    
    except Exception as e:
        print(f"Error fetching info for {ticker_symbol}: {str(e)}")
        return None


def validate_ticker(ticker_symbol):
    """
    Check if a ticker symbol is valid by attempting to fetch its info
    
    Args:
        ticker_symbol (str): Stock ticker symbol to validate
    
    Returns:
        bool: True if ticker is valid, False otherwise
    
    Example:
        >>> validate_ticker('AAPL')  # True
        >>> validate_ticker('INVALID123')  # False
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        # Try to get info - if ticker invalid, this will fail
        info = ticker.info
        
        # Check if we got meaningful data
        # Invalid tickers return empty or minimal info
        if 'symbol' in info or 'shortName' in info:
            return True
        return False
    
    except:
        return False


def get_multiple_stocks_data(ticker_list, start_date, end_date):
    """
    Fetch historical data for multiple stock tickers
    
    Args:
        ticker_list (list): List of ticker symbols
        start_date (datetime): Start date
        end_date (datetime): End date
    
    Returns:
        dict: Dictionary with ticker symbols as keys and DataFrames as values
              Format: {'AAPL': DataFrame, 'GOOGL': DataFrame, ...}
    
    Example:
        >>> tickers = ['AAPL', 'GOOGL', 'MSFT']
        >>> data = get_multiple_stocks_data(tickers, start_date, end_date)
        >>> print(data['AAPL'].head())
    """
    stock_data = {}
    
    for ticker in ticker_list:
        data = get_stock_data(ticker, start_date, end_date)
        if data is not None:
            stock_data[ticker] = data
    
    return stock_data


# For testing this module directly
if __name__ == "__main__":
    # Testing with Apple stock
    print("Testing data collection module...")
    
    # Testing dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Last 30 days
    
    # Testing for single stock
    print("\n1. Fetching AAPL data...")
    data = get_stock_data('AAPL', start_date, end_date)
    if data is not None:
        print(f"Success! Got {len(data)} days of data")
        print(data.head())
    else:
        print("Failed to fetch data")
    
    # Testing stock info
    print("\n2. Fetching AAPL company info...")
    info = get_stock_info('AAPL')
    if info:
        print(f"Company: {info.get('longName', 'N/A')}")
        print(f"Sector: {info.get('sector', 'N/A')}")
    
    # Testing validation
    print("\n3. Testing ticker validation...")
    print(f"AAPL valid: {validate_ticker('AAPL')}")
    print(f"INVALID123 valid: {validate_ticker('INVALID123')}")