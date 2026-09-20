# Credit Risk Securitisation Analytics

## Overview

An end-to-end credit risk analytics project covering Expected Credit Loss (ECL) modelling, portfolio risk analysis, stress testing, securitisation tranche analysis, and Power BI dashboard reporting.

The project uses a synthetic loan portfolio of 5,000 loans and demonstrates how loan-level risk data can be transformed into portfolio-level credit risk insights.

## Key Areas

- Expected Credit Loss (ECL) modelling
- PD, LGD and EAD analysis
- Credit risk segmentation
- Credit score, LTV and DPD analysis
- Stress testing
- Securitisation tranche analysis
- Base and stress waterfall analysis
- Power BI dashboard development
- Portfolio risk reporting

## Portfolio Summary

- **Total Loans:** 5,000
- **Total Exposure:** ₹231.45M
- **Total ECL:** ₹7.68M
- **ECL / Exposure:** 3.32%
- **Default Rate:** 30.36%

## Stress Testing

Three analytical scenarios are used:

| Scenario | PD Multiplier | LGD Multiplier |
|---|---:|---:|
| Base | 1.00x | 1.00x |
| Moderate Stress | 1.30x | 1.10x |
| Severe Stress | 1.70x | 1.25x |

## Securitisation Analysis

A simplified analytical tranche structure is used:

- **Senior:** 70%
- **Mezzanine:** 20%
- **Equity:** 10%

Portfolio losses are allocated through the simplified waterfall from Equity to Mezzanine and then Senior.

> The securitisation structure is an analytical prototype and does not represent actual transaction or legal terms.

## Technology

- Python
- Pandas
- NumPy
- Scikit-learn
- Power BI
- SQL
- Excel

## Project Structure

```text
credit-risk-securitisation-analytics/
├── data/
├── docs/
├── powerbi/
├── reports/
├── sql/
├── src/
├── tests/
└── README.md

Disclaimer
This project uses a synthetic loan portfolio. Stress scenarios, ECL assumptions, and securitisation waterfall mechanics are designed for analytical and portfolio demonstration purposes and should not be interpreted as actual lending, investment, or transaction advice.
