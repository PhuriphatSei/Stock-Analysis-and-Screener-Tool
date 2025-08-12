import os
import yfinance as yf
import pandas as pd
from valuation_dcf import dcf_valuation
from valuation_graham import graham_valuation
from pe_roe_trend import plot_pe_roe_trend
from sector_heatmap import sector_heatmap
from analyst_report import create_analyst_report

# กำหนดโฟลเดอร์เก็บไฟล์
output_dir = r"C:\Users\Lenovo\Desktop\Project\Portfolio_Group\set50\set50\output"
csv_dir = r"C:\Users\Lenovo\Desktop\Project\Portfolio_Group\set50\set50\data\raw"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(csv_dir, exist_ok=True)

# รายชื่อหุ้นไทยที่สนใจ
stocks = ["TCAP.BK", "KBANK.BK", "BBL.BK", "SCB.BK"]

# อัตราผลตอบแทนพันธบัตร 10 ปี (ตามจริง ณ มี.ค. 2025)
risk_free_rate = 0.02085  # 2.085%

# ผลตอบแทนตลาด (ประมาณ conservative)
market_return = 0.10  # 10%

# อัตราการเติบโตระยะยาว
growth_rate = 0.04  # 4%

results = []

for symbol in stocks:
    print(f"Fetching data for {symbol}...")
    stock = yf.Ticker(symbol)

    try:
        info = stock.info
    except Exception as e:
        print(f"Error fetching info for {symbol}: {e}")
        continue

    price = info.get("currentPrice", None)
    pe_ratio = info.get("trailingPE", None)
    pb_ratio = info.get("priceToBook", None)
    roe = info.get("returnOnEquity", None)
    eps = info.get("trailingEps", None)
    book_value = info.get("bookValue", None)
    shares_outstanding = info.get("sharesOutstanding", None)
    net_income = info.get("netIncomeToCommon", None)
    sector = info.get("sector", "N/A")

    # คำนวณ DCF Value
    if eps and shares_outstanding:
        dcf_value = dcf_valuation(
            eps=eps,
            growth_rate=growth_rate,
            discount_rate=market_return,
            years=5,
            shares_outstanding=shares_outstanding
        )
    else:
        dcf_value = None

    # คำนวณ Graham Value
    if eps and book_value:
        graham_value = graham_valuation(eps, book_value)
    else:
        graham_value = None

    results.append({
        "Symbol": symbol,
        "Sector": sector,
        "Price": price,
        "PE": pe_ratio,
        "PBV": pb_ratio,
        "ROE": roe,
        "EPS": eps,
        "Book Value": book_value,
        "Net Income": net_income,
        "DCF Value": dcf_value,
        "Graham Value": graham_value
    })

    # วาดกราฟ PE-ROE Trend และบันทึกใน output
    try:
        plot_pe_roe_trend(symbol, output_path=os.path.join(output_dir, f"{symbol}_trend.png"))
        print(f"Saved PE-ROE trend chart for {symbol}")
    except Exception as e:
        print(f"Failed to plot PE-ROE trend for {symbol}: {e}")

# สร้าง DataFrame
df = pd.DataFrame(results)

# แปลง ROE เป็น %
df["ROE (%)"] = df["ROE"].apply(lambda x: x * 100 if pd.notnull(x) else None)

# สร้าง sector heatmap และบันทึกไฟล์ใน output
try:
    sector_heatmap(df, output_path=os.path.join(output_dir, "sector_heatmap.png"))
    print("Saved sector heatmap")
except Exception as e:
    print(f"Failed to create sector heatmap: {e}")

# บันทึก CSV ลงใน data/raw
csv_path = os.path.join(csv_dir, "stock_valuation_results.csv")
df.to_csv(csv_path, index=False)
print(f"Stock valuation results saved to '{csv_path}'")

# สร้างรายงาน PDF
try:
    create_analyst_report(df, output_dir=output_dir, filename="analyst_report.pdf")
except Exception as e:
    print(f"Failed to create analyst report PDF: {e}")

print("\n✅ All tasks completed!")
