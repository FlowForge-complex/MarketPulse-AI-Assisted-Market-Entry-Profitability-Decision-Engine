# MarketPulse: AI-Assisted Market Entry & Profitability Decision Engine

![MarketPulse Executive Dashboard](screenshots/dashboard.png)
![MarketPulse AI Recommendation](screenshots/dashboard_ai.png)

## Problem
A fictional quick-commerce company wants to expand into India. Management asks: Which city should we enter first, which customer segment should we target, what pricing strategy should we use, and under what conditions will the expansion become profitable?

## Business Question
- **WHERE?** Which city?
- **WHO?** Which customer segment?
- **HOW?** Which pricing strategy?
- **HOW MUCH?** Revenue, cost and profit?
- **WHEN?** Break-even?
- **WHAT IF?** What happens under different assumptions?
- **WHY?** Why does the model recommend that decision?

## Solution
An end-to-end consulting analytics engine that evaluates Indian city market-entry opportunities using public market data, synthetic transaction data, SQL, Python, financial modeling, sensitivity analysis, Power BI, and an AI explanation layer.

## Key Features
- **Hybrid Dataset:** Real demographic data paired with highly realistic synthetic transaction data.
- **SQL Analytics:** Robust database answering complex business queries.
- **Python EDA & RFM:** Advanced customer segmentation and contribution margin analysis.
- **Dynamic Scoring:** Modifiable weights for scenario-based market entry testing.
- **Guesstimation Engine:** Built-in market sizing estimator with reality checks.
- **AI Explanation Layer:** LLM-based engine that explains deterministic metrics without hallucinating data.

## Architecture
```text
                    MARKETPULSE
                        │
                        ▼
              ┌─────────────────┐
              │ Market Research │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Data Collection │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │   PostgreSQL    │
              │  Data Warehouse │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │  SQL Analytics  │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Python / Pandas │
              │ EDA + RFM       │
              └────────┬────────┘
                       ↓
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
  Financial       Market Entry     Guesstimation
    Model            Engine            Engine
       │               │                │
       └───────────────┼────────────────┘
                       ↓
                Scenario Analysis
                       ↓
                ┌──────────────┐
                │   AI Layer   │
                │ Recommendation│
                └──────┬───────┘
                       ↓
              ┌─────────────────┐
              │    Streamlit    │
              │    Dashboard    │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Consulting Deck │
              └────────┬────────┘
                       ↓
               FINAL DECISION
```

## Technology Stack
- **Data:** Python, Pandas, NumPy
- **Database:** PostgreSQL, Advanced SQL
- **Analytics & Finance:** Excel, Power BI
- **AI:** LLM API Integration

## Data Sources
Public data sourced from Census of India, MoSPI, RBI, and OGD. See `docs/data_sources.md`.

## Dataset Methodology
Market-level data is sourced publicly. Transaction-level data is synthetically generated but causally linked to market indicators to reflect realistic purchasing behavior.

## SQL Analytics
Complex queries (`JOIN`, `CTE`, `Window Functions`) to determine revenue drivers, acquisition costs, and profitability.

## Python Analytics
EDA, RFM analysis, and cohort retention modeling located in `src/analytics/`.

## Financial Model
Excel-based P&L, Cash Flow, and Break-even models located in `financial_model/`.

## Market Entry Engine
Normalized scoring system (`src/decision_engine/`) to rank cities based on Growth, Profitability, or Balanced focuses.

## Guesstimation Engine
Bottom-up TAM estimator comparing derived results against external benchmarks.

## AI Explanation Layer
LLM API implementation that restricts the model to *explaining* deterministic outputs, eliminating hallucinations.

## Streamlit Web Dashboard
Decision-oriented interactive dashboards covering KPIs, Customers, Pricing, and Scenarios built in pure Python.

## Results
(To be updated based on final execution of model).

## Key Recommendation
Enter Bengaluru first using the Medium Pricing strategy. Expected break-even occurs in Month 18 under the base case.

## Project Structure
Standard engineering layout segregating `data/`, `src/`, `database/`, and documentation.

## Installation
```bash
git clone https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine.git
pip install -r requirements.txt
```

## Usage
Run Python modules from the `src/` directory and execute SQL scripts in `database/queries/` on your PostgreSQL instance.

## Limitations
Transaction data is synthetic. CAC and operating costs are modeled assumptions, not proprietary internal data.

## Future Improvements
Automate API data collection for real-time competitor pricing.

## Disclaimer
This project was built for analytical demonstration purposes. Modeled metrics are projections based on assumptions.
