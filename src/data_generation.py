import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

N = 5000

data = pd.DataFrame({
    "loan_id": [f"LN{i:06d}" for i in range(1, N + 1)],
    "customer_id": [f"CUST{i:06d}" for i in range(1, N + 1)],
    "asset_type": np.random.choice(
        ["Auto Loan", "Mortgage", "Structured Credit"],
        size=N,
        p=[0.40, 0.40, 0.20]
    ),
    "loan_amount": np.round(
        np.random.lognormal(mean=10.5, sigma=0.7, size=N), 2
    ),
    "interest_rate": np.round(
        np.random.uniform(5, 12, size=N), 2
    ),
    "loan_term_months": np.random.choice(
        [36, 48, 60, 120, 180, 240, 360],
        size=N
    ),
    "credit_score": np.random.randint(550, 851, size=N),
    "annual_income": np.round(
        np.random.uniform(250000, 2500000, size=N), 2
    ),
    "days_past_due": np.random.choice(
        [0, 0, 0, 0, 30, 60, 90, 120],
        size=N
    ),
    "ltv": np.round(
        np.random.uniform(40, 100, size=N), 2
    ),
    "unemployment_rate": np.round(
        np.random.uniform(3, 9, size=N), 2
    )
})

# Default indicator
default_probability = (
    0.02
    + np.where(data["credit_score"] < 650, 0.06, 0)
    + np.where(data["days_past_due"] >= 90, 0.15, 0)
    + np.where(data["ltv"] > 80, 0.04, 0)
    + np.where(data["unemployment_rate"] > 7, 0.03, 0)
)

default_probability = np.clip(default_probability, 0, 0.60)

data["default_probability"] = np.round(default_probability, 4)

data["default_flag"] = (
    np.random.random(N) < default_probability
).astype(int)

# LGD assumption
data["lgd"] = np.round(
    np.clip(
        0.25
        + np.where(data["ltv"] > 80, 0.15, 0)
        + np.where(data["asset_type"] == "Structured Credit", 0.10, 0),
        0.20,
        0.80
    ),
    4
)

# EAD approximation
data["ead"] = np.round(data["loan_amount"], 2)

# Simplified expected credit loss
data["ecl"] = np.round(
    data["default_probability"]
    * data["lgd"]
    * data["ead"],
    2
)

# IFRS 9-style staging proxy
data["stage"] = np.select(
    [
        data["days_past_due"] >= 90,
        data["days_past_due"] >= 30,
    ],
    [
        3,
        2,
    ],
    default=1
)

# Create output folder
output_path = Path("data/processed")
output_path.mkdir(parents=True, exist_ok=True)

# Save dataset
file_path = output_path / "loan_portfolio.csv"
data.to_csv(file_path, index=False)

print("=" * 60)
print("SECURITISATION DATASET CREATED")
print("=" * 60)
print(f"Records: {len(data):,}")
print(f"Columns: {len(data.columns)}")
print(f"Total Exposure: ₹{data['ead'].sum():,.2f}")
print(f"Total ECL: ₹{data['ecl'].sum():,.2f}")
print()
print("Asset Type Distribution:")
print(data["asset_type"].value_counts())
print()
print("Stage Distribution:")
print(data["stage"].value_counts().sort_index())
print()
print(f"Saved to: {file_path}")