# Credit Risk Analytics & Securitisation Waterfall Analysis

## Project Overview

This project presents an end-to-end credit risk analytics framework for a synthetic loan portfolio of 5,000 loans.

The project covers:

- Expected Credit Loss (ECL) modelling
- Credit risk segmentation
- Stress testing
- Securitisation tranche analysis
- Waterfall loss allocation
- Power BI dashboard development

## Portfolio Summary

| Metric | Value |
|---|---:|
| Number of Loans | 5,000 |
| Total Exposure (EAD) | ₹231.45 Million |
| Total ECL | ₹7.68 Million |
| Average ECL | ₹1,536.88 |
| ECL / Exposure | 3.32% |
| Default Rate | 30.36% |

## ECL Methodology

Expected Credit Loss is calculated using:

ECL = PD × LGD × EAD

Where:

- PD = Probability of Default
- LGD = Loss Given Default
- EAD = Exposure at Default

## Risk Analysis

Portfolio risk is analyzed across:

- Asset Type
- Credit Score
- Loan-to-Value (LTV)
- Days Past Due (DPD)
- Credit Risk Stage

## Stress Testing

Three analytical scenarios are used:

| Scenario | PD Multiplier | LGD Multiplier |
|---|---:|---:|
| Base | 1.00x | 1.00x |
| Moderate Stress | 1.30x | 1.10x |
| Severe Stress | 1.70x | 1.25x |

These scenarios are illustrative analytical assumptions and are not forecasts.

## Securitisation Structure

The prototype uses:

- Senior: 70%
- Mezzanine: 20%
- Equity: 10%

Losses are allocated sequentially from Equity to Mezzanine and then Senior.

This is a simplified analytical prototype and does not represent actual legal or transaction terms.

## Power BI Dashboard

The dashboard contains four pages:

1. Credit Risk Dashboard
2. Stress Testing & Securitisation Analysis
3. Risk Analysis
4. Portfolio & ECL Summary

## Tools & Technologies

- Python
- Pandas
- NumPy
- SQL
- Power BI
- DAX
- Credit Risk Analytics
- ECL Modelling

## Project Deliverables

- Power BI dashboard
- Professional project report
- Analytical reports and datasets
- Python/SQL source files

## Important Note

This project uses a synthetic loan portfolio for analytical and educational purposes. The results should not be interpreted as lending, investment, or transaction advice.
