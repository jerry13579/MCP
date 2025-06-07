from mcp.server.fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("stockserver")
   

@mcp.tool()
def current_stock_price(stock_ticker: str) -> str:
    """This tool returns the last known price for a given stock ticker.
    Args:
        stock_ticker: an alphanumeric stock ticker 
        Example payload: "TSLA"
    Returns:
        str:"Current price for Ticker: Last Price" 
        Example response: "Current price for TSLA: 1000.0"
        """
    stock_ticker = stock_ticker.strip().upper()
    try:
        ticker = yf.Ticker(stock_ticker)
        last_price = ticker.info['regularMarketPrice']
        return f"Current price for {stock_ticker}: {last_price}"
    except Exception as e:
        return f"Error fetching data for {stock_ticker}: {e}"
'''
@mcp.tool()
def stock_price_performance(stock_ticker: str, time_range: str) -> str:
    """This tool returns the past period of daily percent changes for a given stock ticker.
    Args:
        stock_ticker: a stock ticker symbol Yahoo Finance recognizes
        range: a string of '1d', '5d', '1mo', '3mo', '6mo', '1y', '5y'
        Example payload: "TSLA", "3mo"
    Returns:
        str: JSON string of daily percent changes
        Example response: {
            "ticker": stock_ticker,
            "daily_percent_changes": ticker_change,
        }
        """
    stock_ticker = stock_ticker.strip().upper()
    ticker = Ticker(ticker=stock_ticker)
    data = ticker.yahoo_api_price(range=time_range, dataGranularity='1d')
    ticker_change = ((data['close'] - data['open']) / data['open'] * 100).round(2).tolist()
    
    return {
        "ticker": stock_ticker,
        "daily_percent_changes": ticker_change,
    }


'''

@mcp.tool()
def sentiment_analysis(stock_ticker: str) -> str:
    """This tool returns the sentiment analysis for a given stock ticker.
    Args:
        stock_ticker: a stock ticker symbol Yahoo Finance recognizes
        Example payload: "TSLA"
    Returns:
        str: sentiment 
        """
    return f"The sentiment for {stock_ticker} is very positive!"



if __name__ == "__main__":
    mcp.run(transport="stdio")