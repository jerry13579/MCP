from mcp.server.fastmcp import FastMCP
from stockdex import Ticker
import json

mcp = FastMCP("stockserver")

@mcp.prompt()
def stock_trade_advice(stock_data:str) -> str:
    """Prompt template for any stock trade advice inquiry"""
    return f"""You are a helpful financial assistant designed to recommend stock trades.
               Using the information below, recommend a stock trade based on the user's inquiry with a detailed explanation. Also include a hilariously funny joke about the stock performance
                Data {stock_data}"""
                

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
    ticker = Ticker(ticker=stock_ticker)
    last_price = ticker.yahoo_api_price(range='1h', dataGranularity='1h').sort_values('timestamp', ascending=False).iloc[0]['close'].round(2)
    return f"Current price for {stock_ticker}: {last_price}"

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



if __name__ == "__main__":
    mcp.run(transport="stdio")