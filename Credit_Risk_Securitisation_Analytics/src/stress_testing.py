import pandas as pd
from pathlib import Path

# Load portfolio
df = pd.read_csv("data/processed/loan_portfolio.csv")

print("=" * 65)
print("SECURITISATION PORTFOLIO STRESS TEST")
print("=" * 65)

# Original portfolio values
base_ecl = df["ecl"].sum()
base_exposure = df["ead"].sum()

# Stress scenarios
scenarios = {
    "Base": {
        "pd_multiplier": 1.00,
        "lgd_multiplier": 1.00
    },
    "Moderate Stress": {
        "pd_multiplier": 1.30,
        "lgd_multiplier": 1.10
    },
    "Severe Stress": {
        "pd_multiplier": 1.70,
        "lgd_multiplier": 1.25
    }
}

results = []

for scenario, assumptions in scenarios.items():

    stressed_pd = (
        df["default_probability"]
        * assumptions["pd_multiplier"]
    ).clip(upper=1.0)

    stressed_lgd = (
        df["lgd"]
        * assumptions["lgd_multiplier"]
    ).clip(upper=1.0)

    stressed_ecl = (
        stressed_pd
        * stressed_lgd
        * df["ead"]
    )

    total_ecl = stressed_ecl.sum()

    results.append({
        "Scenario": scenario,
        "PD Multiplier": assumptions["pd_multiplier"],
        "LGD Multiplier": assumptions["lgd_multiplier"],
        "Exposure": base_exposure,
        "Stressed ECL": total_ecl,
        "ECL Rate (%)": total_ecl / base_exposure * 100,
        "Increase vs Base (%)":
            (total_ecl / base_ecl - 1) * 100
    })

results_df = pd.DataFrame(results)

print("\nSTRESS TEST RESULTS")
print(results_df.to_string(index=False))

# --------------------------------------------------
# Asset-level severe stress
# --------------------------------------------------

severe_pd = (
    df["default_probability"] * 1.70
).clip(upper=1.0)

severe_lgd = (
    df["lgd"] * 1.25
).clip(upper=1.0)

df["severe_stress_ecl"] = (
    severe_pd
    * severe_lgd
    * df["ead"]
)

asset_stress = (
    df.groupby("asset_type")
    .agg(
        Loans=("loan_id", "count"),
        Exposure=("ead", "sum"),
        Severe_Stress_ECL=("severe_stress_ecl", "sum")
    )
    .reset_index()
)

asset_stress["Stress_ECL_Rate_%"] = (
    asset_stress["Severe_Stress_ECL"]
    / asset_stress["Exposure"]
    * 100
)

print("\nSEVERE STRESS BY ASSET TYPE")
print(asset_stress.to_string(index=False))

# Save results
Path("reports").mkdir(exist_ok=True)

results_df.to_csv(
    "reports/stress_test_results.csv",
    index=False
)

asset_stress.to_csv(
    "reports/severe_stress_by_asset.csv",
    index=False
)

print("\n" + "=" * 65)
print("STRESS TEST COMPLETED SUCCESSFULLY")
print("=" * 65)

print("\nReports saved:")
print("reports/stress_test_results.csv")
print("reports/severe_stress_by_asset.csv")