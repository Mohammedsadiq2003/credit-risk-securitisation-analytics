import pandas as pd
from pathlib import Path

# Load portfolio
df = pd.read_csv("data/processed/loan_portfolio.csv")

print("=" * 65)
print("SECURITISATION PORTFOLIO RISK ANALYSIS")
print("=" * 65)

# 1. Risk by asset type
asset_risk = (
    df.groupby("asset_type")
    .agg(
        Loans=("loan_id", "count"),
        Exposure=("loan_amount", "sum"),
        Defaults=("default_flag", "sum"),
        ECL=("ecl", "sum"),
    )
    .reset_index()
)

asset_risk["Default_Rate_%"] = (
    asset_risk["Defaults"] / asset_risk["Loans"] * 100
)

asset_risk["ECL_Rate_%"] = (
    asset_risk["ECL"] / asset_risk["Exposure"] * 100
)

print("\nRISK BY ASSET TYPE")
print(asset_risk.to_string(index=False))

# 2. Risk by IFRS 9 stage
stage_risk = (
    df.groupby("stage")
    .agg(
        Loans=("loan_id", "count"),
        Exposure=("loan_amount", "sum"),
        Defaults=("default_flag", "sum"),
        ECL=("ecl", "sum"),
    )
    .reset_index()
)

stage_risk["Default_Rate_%"] = (
    stage_risk["Defaults"] / stage_risk["Loans"] * 100
)

stage_risk["ECL_Rate_%"] = (
    stage_risk["ECL"] / stage_risk["Exposure"] * 100
)

print("\nRISK BY IFRS 9 STAGE")
print(stage_risk.to_string(index=False))

# 3. Credit score bands
df["credit_score_band"] = pd.cut(
    df["credit_score"],
    bins=[0, 580, 670, 740, 850],
    labels=["Poor", "Fair", "Good", "Very Good"],
    include_lowest=True
)

credit_risk = (
    df.groupby("credit_score_band", observed=False)
    .agg(
        Loans=("loan_id", "count"),
        Defaults=("default_flag", "sum"),
        Exposure=("loan_amount", "sum"),
        ECL=("ecl", "sum"),
    )
    .reset_index()
)

credit_risk["Default_Rate_%"] = (
    credit_risk["Defaults"] / credit_risk["Loans"] * 100
)

credit_risk["ECL_Rate_%"] = (
    credit_risk["ECL"] / credit_risk["Exposure"] * 100
)

print("\nRISK BY CREDIT SCORE")
print(credit_risk.to_string(index=False))

# 4. LTV bands
df["ltv_band"] = pd.cut(
    df["ltv"],
    bins=[0, 60, 80, 100, float("inf")],
    labels=["Low LTV", "Moderate LTV", "High LTV", "Very High LTV"],
    include_lowest=True
)

ltv_risk = (
    df.groupby("ltv_band", observed=False)
    .agg(
        Loans=("loan_id", "count"),
        Defaults=("default_flag", "sum"),
        Exposure=("loan_amount", "sum"),
        ECL=("ecl", "sum"),
    )
    .reset_index()
)

ltv_risk["Default_Rate_%"] = (
    ltv_risk["Defaults"] / ltv_risk["Loans"] * 100
)

ltv_risk["ECL_Rate_%"] = (
    ltv_risk["ECL"] / ltv_risk["Exposure"] * 100
)

print("\nRISK BY LTV")
print(ltv_risk.to_string(index=False))

# 5. Delinquency bands
df["dpd_band"] = pd.cut(
    df["days_past_due"],
    bins=[-1, 0, 30, 60, 90, float("inf")],
    labels=["Current", "1-30 Days", "31-60 Days", "61-90 Days", "90+ Days"]
)

dpd_risk = (
    df.groupby("dpd_band", observed=False)
    .agg(
        Loans=("loan_id", "count"),
        Defaults=("default_flag", "sum"),
        Exposure=("loan_amount", "sum"),
        ECL=("ecl", "sum"),
    )
    .reset_index()
)

dpd_risk["Default_Rate_%"] = (
    dpd_risk["Defaults"] / dpd_risk["Loans"] * 100
)

dpd_risk["ECL_Rate_%"] = (
    dpd_risk["ECL"] / dpd_risk["Exposure"] * 100
)

print("\nRISK BY DELINQUENCY")
print(dpd_risk.to_string(index=False))

# Save reports
Path("reports").mkdir(exist_ok=True)

asset_risk.to_csv("reports/risk_by_asset_type.csv", index=False)
stage_risk.to_csv("reports/risk_by_stage.csv", index=False)
credit_risk.to_csv("reports/risk_by_credit_score.csv", index=False)
ltv_risk.to_csv("reports/risk_by_ltv.csv", index=False)
dpd_risk.to_csv("reports/risk_by_dpd.csv", index=False)

print("\n" + "=" * 65)
print("RISK ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 65)