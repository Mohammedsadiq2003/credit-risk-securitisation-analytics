import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create charts folder
Path("reports/charts").mkdir(parents=True, exist_ok=True)

# Load main dataset
df = pd.read_csv("data/processed/loan_portfolio.csv")

print("=" * 65)
print("SECURITISATION RISK VISUALIZATION")
print("=" * 65)

# ---------------------------------------------------------
# 1. ECL BY ASSET TYPE
# ---------------------------------------------------------
ecl_asset = (
    df.groupby("asset_type")["ecl"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 6))
ecl_asset.plot(kind="bar")
plt.title("Expected Credit Loss by Asset Type")
plt.xlabel("Asset Type")
plt.ylabel("Expected Credit Loss (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("reports/charts/ecl_by_asset_type.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# 2. ECL BY STAGE
# ---------------------------------------------------------
ecl_stage = (
    df.groupby("stage")["ecl"]
    .sum()
)

plt.figure(figsize=(8, 6))
ecl_stage.plot(kind="bar")
plt.title("Expected Credit Loss by IFRS 9 Stage")
plt.xlabel("Stage")
plt.ylabel("Expected Credit Loss (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("reports/charts/ecl_by_stage.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# 3. DEFAULT RATE BY CREDIT SCORE BAND
# ---------------------------------------------------------
df["credit_score_band"] = pd.cut(
    df["credit_score"],
    bins=[0, 599, 649, 699, 749, 799, 900],
    labels=[
        "<600",
        "600-649",
        "650-699",
        "700-749",
        "750-799",
        "800+"
    ]
)

default_by_score = (
    df.groupby("credit_score_band", observed=False)["default_flag"]
    .mean() * 100
)

plt.figure(figsize=(9, 6))
default_by_score.plot(kind="bar")
plt.title("Default Rate by Credit Score Band")
plt.xlabel("Credit Score Band")
plt.ylabel("Default Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("reports/charts/default_rate_credit_score.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# 4. ECL BY LTV BAND
# ---------------------------------------------------------
df["ltv_band"] = pd.cut(
    df["ltv"],
    bins=[0, 60, 70, 80, 90, 100],
    labels=[
        "<=60%",
        "60-70%",
        "70-80%",
        "80-90%",
        "90-100%"
    ]
)

ecl_by_ltv = (
    df.groupby("ltv_band", observed=False)["ecl"]
    .sum()
)

plt.figure(figsize=(9, 6))
ecl_by_ltv.plot(kind="bar")
plt.title("Expected Credit Loss by LTV Band")
plt.xlabel("LTV Band")
plt.ylabel("Expected Credit Loss (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("reports/charts/ecl_by_ltv.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# 5. EXPOSURE BY ASSET TYPE
# ---------------------------------------------------------
exposure_asset = (
    df.groupby("asset_type")["ead"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 6))
exposure_asset.plot(kind="bar")
plt.title("Exposure at Default by Asset Type")
plt.xlabel("Asset Type")
plt.ylabel("Exposure (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("reports/charts/exposure_by_asset_type.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# 6. STRESS TEST RESULTS
# ---------------------------------------------------------
stress_file = Path("reports/stress_test_results.csv")

if stress_file.exists():
    stress = pd.read_csv(stress_file)

    print("\nStress Test Results:")
    print(stress.to_string(index=False))

    # Try to identify scenario and loss columns
    scenario_col = None
    loss_col = None

    for col in stress.columns:
        if col.lower() in ["scenario", "stress_scenario"]:
            scenario_col = col
        if "ecl" in col.lower() or "loss" in col.lower():
            loss_col = col

    if scenario_col and loss_col:
        plt.figure(figsize=(9, 6))
        plt.bar(stress[scenario_col].astype(str), stress[loss_col])
        plt.title("Securitisation Stress Test")
        plt.xlabel("Scenario")
        plt.ylabel("Expected Loss (₹)")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.savefig("reports/charts/stress_test.png", dpi=300)
        plt.close()

print("\n" + "=" * 65)
print("VISUALIZATION COMPLETED SUCCESSFULLY")
print("=" * 65)

print("\nCharts saved in:")
print("reports/charts/")
print("\nCreated charts:")
print("1. ecl_by_asset_type.png")
print("2. ecl_by_stage.png")
print("3. default_rate_credit_score.png")
print("4. ecl_by_ltv.png")
print("5. exposure_by_asset_type.png")
print("6. stress_test.png (if stress-test columns are detected)")