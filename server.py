from mcp.server.fastmcp import FastMCP
from stockdex import Ticker


# Create server 
mcp = FastMCP("stockserver")

# Build server function
@mcp.tool()
def current_stock_price(stock_ticker: str) -> str:
    """This tool returns the last known price for a given stock ticker.
    Args:
        stock_ticker: an alphanumeric stock ticker 
    Returns:
        str:"Ticker: Last Price" 
        """
    stock_ticker = stock_ticker.strip().upper()
    ticker = Ticker(ticker=stock_ticker)
    last_price = ticker.yahoo_api_price(range='1h', dataGranularity='1h').sort_values('timestamp', ascending=False).iloc[0]['close'].round(2)
    return f"Current price for {stock_ticker}: {last_price}"

@mcp.tool()
def stock_price_3mo(stock_ticker: str) -> str:
    """This tool returns the past 3 months of stock price data for a given stock ticker.
    Args:
        stock_ticker: an alphanumeric stock ticker 
    Returns:
        str:"Ticker: daily % change" 
        """
    stock_ticker = stock_ticker.strip().upper()
    def calculate_change(ticker):
        ticker = Ticker(ticker=ticker)
        data = ticker.yahoo_api_price(range='3mo', dataGranularity='1d')
        return ((data['close'] - data['open']) / data['open'] * 100)
    ticker_change = calculate_change(stock_ticker).round(2)
    ticker_vs_index = (ticker_change - calculate_change('^GSPC')).round(2)
    return f"Daily % change for {stock_ticker}: {ticker_change.tolist()}\nDaily % change compared to S&P 500: {ticker_vs_index.tolist()}"


# Kick off server if file is run 
if __name__ == "__main__":
    mcp.run(transport="stdio")