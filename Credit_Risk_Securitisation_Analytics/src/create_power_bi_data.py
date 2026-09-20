import pandas as pd
from pathlib import Path

print("=" * 65)
print("CREATING POWER BI DATA WORKBOOK")
print("=" * 65)

output_folder = Path("powerbi")
output_folder.mkdir(exist_ok=True)

# Load main dataset
df = pd.read_csv("data/processed/loan_portfolio.csv")

# Load analytical reports
ecl_summary = pd.read_csv("reports/ecl_summary.csv")
ecl_asset = pd.read_csv("reports/ecl_by_asset_type.csv")
ecl_stage = pd.read_csv("reports/ecl_by_stage.csv")

risk_asset = pd.read_csv("reports/risk_by_asset_type.csv")
risk_stage = pd.read_csv("reports/risk_by_stage.csv")
risk_score = pd.read_csv("reports/risk_by_credit_score.csv")
risk_ltv = pd.read_csv("reports/risk_by_ltv.csv")
risk_dpd = pd.read_csv("reports/risk_by_dpd.csv")

stress = pd.read_csv("reports/stress_test_results.csv")
stress_asset = pd.read_csv("reports/severe_stress_by_asset.csv")

tranches = pd.read_csv("reports/tranche_structure.csv")
base_waterfall = pd.read_csv("reports/base_waterfall.csv")
stress_waterfall = pd.read_csv("reports/stress_waterfall.csv")

# Create Excel workbook
output_file = output_folder / "securitisation_powerbi_data.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    df.to_excel(
        writer,
        sheet_name="Loan Portfolio",
        index=False
    )

    ecl_summary.to_excel(
        writer,
        sheet_name="ECL Summary",
        index=False
    )

    ecl_asset.to_excel(
        writer,
        sheet_name="ECL by Asset",
        index=False
    )

    ecl_stage.to_excel(
        writer,
        sheet_name="ECL by Stage",
        index=False
    )

    risk_asset.to_excel(
        writer,
        sheet_name="Risk by Asset",
        index=False
    )

    risk_stage.to_excel(
        writer,
        sheet_name="Risk by Stage",
        index=False
    )

    risk_score.to_excel(
        writer,
        sheet_name="Risk by Score",
        index=False
    )

    risk_ltv.to_excel(
        writer,
        sheet_name="Risk by LTV",
        index=False
    )

    risk_dpd.to_excel(
        writer,
        sheet_name="Risk by DPD",
        index=False
    )

    stress.to_excel(
        writer,
        sheet_name="Stress Test",
        index=False
    )

    stress_asset.to_excel(
        writer,
        sheet_name="Stress by Asset",
        index=False
    )

    tranches.to_excel(
        writer,
        sheet_name="Tranches",
        index=False
    )

    base_waterfall.to_excel(
        writer,
        sheet_name="Base Waterfall",
        index=False
    )

    stress_waterfall.to_excel(
        writer,
        sheet_name="Stress Waterfall",
        index=False
    )

print("\nPower BI workbook created successfully.")
print(f"Location: {output_file}")

print("\nSheets created:")
print("1. Loan Portfolio")
print("2. ECL Summary")
print("3. ECL by Asset")
print("4. ECL by Stage")
print("5. Risk by Asset")
print("6. Risk by Stage")
print("7. Risk by Score")
print("8. Risk by LTV")
print("9. Risk by DPD")
print("10. Stress Test")
print("11. Stress by Asset")
print("12. Tranches")
print("13. Base Waterfall")
print("14. Stress Waterfall")

print("\n" + "=" * 65)
print("POWER BI DATA PREPARATION COMPLETED")
print("=" * 65)