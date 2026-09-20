import pandas as pd
from pathlib import Path

# Load portfolio
df = pd.read_csv("data/processed/loan_portfolio.csv")

print("=" * 65)
print("SECURITISATION WATERFALL & TRANCHE ANALYSIS")
print("=" * 65)

# --------------------------------------------------
# 1. Create securitisation pool
# --------------------------------------------------

total_exposure = df["ead"].sum()

print(f"\nTotal Pool Exposure: ₹{total_exposure:,.2f}")

# Tranche structure
tranches = pd.DataFrame({
    "Tranche": ["Senior", "Mezzanine", "Equity"],
    "Percentage": [0.70, 0.20, 0.10]
})

tranches["Initial_Balance"] = (
    total_exposure * tranches["Percentage"]
)

# --------------------------------------------------
# 2. Calculate base portfolio loss
# --------------------------------------------------

base_loss = df["ecl"].sum()

print(f"Base Expected Loss: ₹{base_loss:,.2f}")

# --------------------------------------------------
# 3. Calculate severe stress loss
# --------------------------------------------------

severe_pd = (
    df["default_probability"] * 1.70
).clip(upper=1.0)

severe_lgd = (
    df["lgd"] * 1.25
).clip(upper=1.0)

severe_loss = (
    severe_pd
    * severe_lgd
    * df["ead"]
).sum()

print(f"Severe Stress Loss: ₹{severe_loss:,.2f}")

# --------------------------------------------------
# 4. Waterfall function
# --------------------------------------------------

def allocate_losses(total_loss, tranche_df):

    remaining_loss = total_loss
    results = []

    # Loss absorption order:
    # Equity -> Mezzanine -> Senior

    absorption_order = [
        ("Equity", 0.10),
        ("Mezzanine", 0.20),
        ("Senior", 0.70)
    ]

    balances = {
        name: total_exposure * percentage
        for name, percentage in absorption_order
    }

    for tranche, percentage in absorption_order:

        absorbed = min(
            remaining_loss,
            balances[tranche]
        )

        remaining_loss -= absorbed

        original_balance = balances[tranche]

        results.append({
            "Tranche": tranche,
            "Initial_Balance": original_balance,
            "Loss_Absorbed": absorbed,
            "Remaining_Balance":
                original_balance - absorbed,
            "Loss_%":
                absorbed / original_balance * 100
        })

    return pd.DataFrame(results)


# --------------------------------------------------
# 5. Base waterfall
# --------------------------------------------------

base_waterfall = allocate_losses(
    base_loss,
    tranches
)

print("\nBASE CASE WATERFALL")
print(base_waterfall.to_string(index=False))

# --------------------------------------------------
# 6. Severe stress waterfall
# --------------------------------------------------

stress_waterfall = allocate_losses(
    severe_loss,
    tranches
)

print("\nSEVERE STRESS WATERFALL")
print(stress_waterfall.to_string(index=False))

# --------------------------------------------------
# 7. Save results
# --------------------------------------------------

Path("reports").mkdir(exist_ok=True)

tranches.to_csv(
    "reports/tranche_structure.csv",
    index=False
)

base_waterfall.to_csv(
    "reports/base_waterfall.csv",
    index=False
)

stress_waterfall.to_csv(
    "reports/stress_waterfall.csv",
    index=False
)

print("\n" + "=" * 65)
print("WATERFALL ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 65)

print("\nReports saved:")
print("reports/tranche_structure.csv")
print("reports/base_waterfall.csv")
print("reports/stress_waterfall.csv")