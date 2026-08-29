# MarketPulse: AI-Assisted Market Entry & Profitability Decision Engine

[![CI Pipeline](https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine/actions/workflows/ci.yml/badge.svg)](https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Coverage](https://img.shields.io/badge/coverage-%3E80%25-brightgreen.svg)](tests/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![MarketPulse Executive Dashboard](screenshots/dashboard.png)
![MarketPulse AI Recommendation](screenshots/dashboard_ai.png)

---

## 1. Problem Overview
A rapidly scaling quick-commerce company intends to expand its operations across tier-1 Indian markets. Management requires a data-driven strategy to answer: Which city should we enter first, which customer segment offers the highest LTV, what is the optimal pricing strategy, and under what conditions does the expansion achieve profitability?

---

## 2. Core Business Questions
- **WHERE?** Which city offers the highest risk-adjusted market attractiveness?
- **WHO?** Which customer segment drives long-term contribution margins?
- **HOW?** What is the optimal pricing strategy across elasticity curves?
- **HOW MUCH?** What are projected revenues, COGS, delivery costs, and net margins?
- **WHEN?** When does the operation achieve break-even?
- **WHAT IF?** How do outcomes shift under different macro and competitive scenarios?
- **WHY?** What is the structured business reasoning behind the algorithm's recommendation?

---

## 3. End-to-End Architecture

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

---

## 4. Benchmark Evaluation & Results

| Metric | Model Finding | Strategic Interpretation |
| :--- | :--- | :--- |
| **Top-Ranked Market** | **Bengaluru (8.42/100.0)** | #1 on digital penetration (75%) and eCommerce adoption (22%). |
| **Runner-Up Market** | Hyderabad (7.91/100.0) | Favorable operating costs and low competitive dark-store saturation. |
| **Total Addressable Market (TAM)** | **₹1,200 Crores** | Derived via bottom-up demographic and category sizing. |
| **Core Customer Segment** | **Frequent Segment** | Represents 25% of users but drives **45.2% of total contribution margin**. |
| **Optimal Pricing Tier** | **Medium (Competitive Parity)** | Balances volume elasticity with sustainable unit margins. |
| **Base Break-Even Horizon** | **Month 18** | Achieved under base CAC (≤ ₹300) and delivery route density. |
| **CAC Sensitivity Threshold** | **₹350 / User** | CAC above ₹350 pushes break-even beyond Month 22. |

---

## 5. Quickstart & Installation

### Option A: Local Python Environment
```bash
# 1. Clone the repository
git clone https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine.git
cd MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine

# 2. Install pinned dependencies from lockfile
pip install -r requirements.lock.txt

# 3. Run the complete headless decision pipeline
python run_pipeline.py --seed 42 --benchmark

# 4. Launch the interactive executive dashboard
streamlit run src/dashboard/app.py
```

### Option B: Docker Compose (Isolated Environment)
```bash
docker compose up --build
```
Access the interactive dashboard at `http://localhost:8501`.

---

## 6. Testing & Quality Assurance

We enforce an **80%+ test coverage threshold** across all modules with automated linting, typing, and security audits:

```bash
# Run unit & integration test suite with coverage enforcement
python -m pytest tests/ -v --cov=src --cov-fail-under=80

# Run code formatters and linters
black --check src/ tests/
isort --check-only src/ tests/
flake8 src/ tests/

# Run static type checking
mypy src/ tests/

# Run security scans
bandit -r src/
pip-audit -r requirements.txt
```

---

## 7. Project Structure

```text
MarketPulse/
├── .devcontainer/          # VS Code DevContainer configuration
├── .github/
│   ├── workflows/          # GitHub Actions CI/CD (matrix test, lint, mypy, audit)
│   └── dependabot.yml      # Automated dependency vulnerability scanning
├── configs/                # Centralized YAML configuration files
├── data/
│   ├── raw/                # Public demographic reference data (MoSPI, Census)
│   ├── processed/          # Cleaned city market & competitor metrics
│   ├── synthetic/          # Causally linked transaction datasets
│   └── benchmarks/         # Exported model evaluation artifacts
├── database/
│   ├── queries/            # Business SQL analytics (01 to 06)
│   ├── schema.sql          # PostgreSQL DDL schema definition
│   └── seed.sql            # Seed scripts and ingestion logic
├── docs/                   # Data dictionary, assumptions, methodology
├── financial_model/        # 13-tab Excel Financial Model (.xlsx)
├── notebooks/              # Interactive Jupyter notebooks for EDA & Modeling
├── presentation/           # 12-slide Consulting Deck (.pptx)
├── screenshots/            # Executive dashboard and recommendation visual captures
├── src/
│   ├── ai/                 # Deterministic AI explanation layer & prompts
│   ├── analytics/          # EDA, RFM segmentation, cohort retention, profitability
│   ├── core/               # Structured logging, typed dataclasses, configuration
│   ├── dashboard/          # Interactive Streamlit executive dashboard
│   ├── data_generation/    # Reproducible customer, product, and order generators
│   ├── decision_engine/    # Multi-criteria scoring, sensitivity, and pricing engines
│   └── guesstimation/      # Bottom-up TAM sizing model
├── tests/                  # Pytest test suite with 80%+ coverage gate
├── .env.example            # Sample production environment variables
├── .flake8                 # Flake8 style configuration
├── .gitignore              # Standard git exclusion rules
├── CHANGELOG.md            # Release version history
├── CONTRIBUTING.md         # Developer contribution guidelines
├── Dockerfile              # Multi-stage production container definition
├── docker-compose.yml      # Multi-container orchestration
├── pyproject.toml          # Unified project & tooling configuration
├── requirements.txt        # Runtime and development dependency declarations
├── requirements.lock.txt   # Pinned dependency lockfile
├── run_pipeline.py         # Headless CLI pipeline runner
└── SECURITY.md             # Security policy and threat modeling
```

---

## 8. License

This project is open-source software licensed under the [MIT License](LICENSE).
