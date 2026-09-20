import pandas as pd
from pathlib import Path

# Load securitisation loan portfolio
input_file = Path("data/processed/loan_portfolio.csv")
output_file = Path("reports/ecl_summary.csv")

df = pd.read_csv(input_file)

# Portfolio-level ECL summary
summary = {
    "Total Loans": len(df),
    "Total Exposure": df["loan_amount"].sum(),
    "Total ECL": df["ecl"].sum(),
    "Average ECL": df["ecl"].mean(),
    "ECL / Exposure (%)": (df["ecl"].sum() / df["loan_amount"].sum()) * 100,
    "Default Rate (%)": df["default_flag"].mean() * 100,
}

print("=" * 60)
print("SECURITISATION ECL ANALYSIS")
print("=" * 60)

for key, value in summary.items():
    if "%" in key:
        print(f"{key}: {value:.2f}%")
    elif "Loans" in key:
        print(f"{key}: {value:,.0f}")
    else:
        print(f"{key}: ₹{value:,.2f}")

# ECL by asset type
asset_summary = (
    df.groupby("asset_type")
    .agg(
        Loans=("loan_id", "count"),
        Exposure=("loan_amount", "sum"),
        ECL=("ecl", "sum"),
        Average_ECL=("ecl", "mean"),
    )
    .reset_index()
)

asset_summary["ECL_Rate_%"] = (
    asset_summary["ECL"] / asset_summary["Exposure"] * 100
)

# ECL by IFRS 9 stage
stage_summary = (
    df.groupby("stage")
    .agg(
        Loans=("loan_id", "count"),
        Exposure=("loan_amount", "sum"),
        ECL=("ecl", "sum"),
    )
    .reset_index()
)

stage_summary["ECL_Rate_%"] = (
    stage_summary["ECL"] / stage_summary["Exposure"] * 100
)

# Create reports folder if needed
Path("reports").mkdir(exist_ok=True)

# Save detailed summaries
asset_summary.to_csv("reports/ecl_by_asset_type.csv", index=False)
stage_summary.to_csv("reports/ecl_by_stage.csv", index=False)

# Save portfolio summary
pd.DataFrame([summary]).to_csv(output_file, index=False)

print("\nECL BY ASSET TYPE:")
print(asset_summary.to_string(index=False))

print("\nECL BY IFRS 9 STAGE:")
print(stage_summary.to_string(index=False))

print("\nReports saved successfully:")
print("reports/ecl_summary.csv")
print("reports/ecl_by_asset_type.csv")
print("reports/ecl_by_stage.csv")