import pandas as pd
from pathlib import Path

print("=" * 65)
print("SECURITISATION PROJECT VALIDATION")
print("=" * 65)

# ---------------------------------------------------------
# 1. Check main dataset
# ---------------------------------------------------------
data_file = Path("data/processed/loan_portfolio.csv")

if not data_file.exists():
    raise FileNotFoundError("Main loan portfolio dataset not found.")

df = pd.read_csv(data_file)

required_columns = [
    "loan_id",
    "customer_id",
    "asset_type",
    "loan_amount",
    "credit_score",
    "days_past_due",
    "ltv",
    "default_probability",
    "default_flag",
    "lgd",
    "ead",
    "ecl",
    "stage"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

print("\n✓ Main dataset found")
print(f"✓ Records: {len(df):,}")
print(f"✓ Columns: {len(df.columns)}")

# ---------------------------------------------------------
# 2. Check missing values
# ---------------------------------------------------------
missing_values = df[required_columns].isnull().sum().sum()

if missing_values != 0:
    raise ValueError(
        f"Dataset contains {missing_values} missing values."
    )

print("✓ Required fields contain no missing values")

# ---------------------------------------------------------
# 3. Validate important numeric conditions
# ---------------------------------------------------------
if (df["loan_amount"] <= 0).any():
    raise ValueError("Invalid loan amount detected.")

if (df["ead"] <= 0).any():
    raise ValueError("Invalid EAD detected.")

if ((df["default_probability"] < 0) |
    (df["default_probability"] > 1)).any():
    raise ValueError("Invalid default probability detected.")

if ((df["lgd"] < 0) |
    (df["lgd"] > 1)).any():
    raise ValueError("Invalid LGD detected.")

if ((df["default_flag"] != 0) &
    (df["default_flag"] != 1)).any():
    raise ValueError("Default flag must contain only 0 or 1.")

if (~df["stage"].isin([1, 2, 3])).any():
    raise ValueError("Stage must be 1, 2, or 3.")

print("✓ Risk variables passed validation")

# ---------------------------------------------------------
# 4. Validate ECL calculation
# ---------------------------------------------------------
calculated_ecl = (
    df["default_probability"] *
    df["lgd"] *
    df["ead"]
)

ecl_difference = (
    calculated_ecl - df["ecl"]
).abs().max()

if ecl_difference > 0.01:
    raise ValueError(
        f"ECL calculation mismatch: {ecl_difference}"
    )

print("✓ ECL calculation validated")

# ---------------------------------------------------------
# 5. Check analytical reports
# ---------------------------------------------------------
required_reports = [
    "reports/ecl_summary.csv",
    "reports/ecl_by_asset_type.csv",
    "reports/ecl_by_stage.csv",
    "reports/risk_by_asset_type.csv",
    "reports/risk_by_stage.csv",
    "reports/risk_by_credit_score.csv",
    "reports/risk_by_ltv.csv",
    "reports/risk_by_dpd.csv",
    "reports/stress_test_results.csv",
    "reports/severe_stress_by_asset.csv",
    "reports/tranche_structure.csv",
    "reports/base_waterfall.csv",
    "reports/stress_waterfall.csv"
]

missing_reports = [
    report for report in required_reports
    if not Path(report).exists()
]

if missing_reports:
    raise FileNotFoundError(
        f"Missing reports: {missing_reports}"
    )

print("✓ Analytical reports found")

# ---------------------------------------------------------
# 6. Check charts
# ---------------------------------------------------------
chart_folder = Path("reports/charts")

if not chart_folder.exists():
    raise FileNotFoundError("Chart folder not found.")

chart_count = len(list(chart_folder.glob("*.png")))

if chart_count == 0:
    raise FileNotFoundError("No visualization charts found.")

print(f"✓ Visualization charts found: {chart_count}")

# ---------------------------------------------------------
# Final result
# ---------------------------------------------------------
print("\n" + "=" * 65)
print("PROJECT VALIDATION PASSED SUCCESSFULLY")
print("=" * 65)

print("\nThe project passed:")
print("✓ Dataset validation")
print("✓ Missing-value validation")
print("✓ Risk-variable validation")
print("✓ ECL calculation validation")
print("✓ Report validation")
print("✓ Visualization validation")