import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def sector_heatmap(df, output_path="output/sector_heatmap.png"):
    sector_perf = df.groupby("Sector")["ROE (%)"].mean().reset_index()

    plt.figure(figsize=(8, 6))
    heatmap_data = sector_perf.pivot_table(values="ROE (%)", index="Sector", aggfunc="mean")
    sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt=".2f")
    plt.title("Sector ROE Heatmap")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
