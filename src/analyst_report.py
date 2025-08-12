from fpdf import FPDF
import os
import pandas as pd

def create_analyst_report(df, output_dir, filename="analyst_report.pdf"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Stock Analyst Report", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Number of stocks: {len(df)}", ln=True)

    pdf.set_font("Arial", "B", 12)
    for _, row in df.iterrows():
        pe = f"{row['PE']:.2f}" if pd.notnull(row["PE"]) else "N/A"
        roe = f"{row['ROE (%)']:.2f}%" if pd.notnull(row["ROE (%)"]) else "N/A"
        symbol = row.get('Symbol') or row.get('Ticker') or 'N/A'
        pdf.cell(0, 10, f"{symbol} - PE: {pe} ROE: {roe}", ln=True)

    pdf.output(output_path)
    print(f"✅ Analyst report saved at {output_path}")
