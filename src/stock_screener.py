import yfinance as yf
import pandas as pd

def screen_stocks(tickers, pe_limit=15, roe_limit=10, debt_to_equity_limit=1.0):
    results = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            pe = info.get("trailingPE", None)
            roe = info.get("returnOnEquity", None)
            de = info.get("debtToEquity", None)
            sector = info.get("sector", "N/A")

            # แปลงค่าและตรวจสอบ
            pe_val = round(pe, 2) if pe is not None else None
            roe_val = round(roe * 100, 2) if roe is not None else None
            de_val = round(de, 2) if de is not None else None

            # เงื่อนไขการกรองหุ้น (ถ้าค่าไม่ครบ ให้ไม่กรองออก)
            passed_filter = True
            if pe_val is not None and pe_val > pe_limit:
                passed_filter = False
            if roe_val is not None and roe_val < roe_limit:
                passed_filter = False
            if de_val is not None and de_val > debt_to_equity_limit:
                passed_filter = False

            results.append({
                "Ticker": ticker,
                "PE": pe_val,
                "ROE (%)": roe_val,
                "Debt/Equity": de_val,
                "Sector": sector,
                "Passed Filter": passed_filter
            })

        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            results.append({
                "Ticker": ticker,
                "PE": None,
                "ROE (%)": None,
                "Debt/Equity": None,
                "Sector": "N/A",
                "Passed Filter": False
            })

    return pd.DataFrame(results)
