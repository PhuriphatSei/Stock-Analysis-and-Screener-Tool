import yfinance as yf
import matplotlib.pyplot as plt

def plot_pe_roe_trend(ticker, output_path="output/pe_roe_trend.png"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5y")
    pe_ratio = stock.info.get("trailingPE", None)
    roe = stock.info.get("returnOnEquity", None)

    plt.figure(figsize=(8, 4))
    plt.plot(hist.index, hist["Close"], label="Close Price")
    plt.title(f"{ticker} Price Trend (PE: {pe_ratio}, ROE: {roe})")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
