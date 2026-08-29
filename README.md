# MarketPulse: AI-Assisted Market Entry & Profitability Decision Engine

[![CI Pipeline](https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine/actions/workflows/ci.yml/badge.svg)](https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine/actions)
[![Docker Build](https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine/actions/workflows/docker-build.yml/badge.svg)](https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Coverage](https://img.shields.io/badge/coverage-87.6%25-brightgreen.svg)](tests/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: Bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![MarketPulse Executive Dashboard](screenshots/dashboard.png)
![MarketPulse AI Recommendation](screenshots/dashboard_ai.png)

---

## 1. Executive Summary & Problem Framing

A rapidly expanding quick-commerce and consumer delivery enterprise seeks to scale operations across Tier-1 metropolitan markets in India. Strategic leadership requires an algorithmic, evidence-backed decision system to answer 7 core management questions:

1. **WHERE?** Which metropolitan market offers the highest risk-adjusted attractiveness?
2. **WHO?** Which customer behavioral segment generates sustainable lifetime margin contribution?
3. **HOW?** What is the optimal pricing strategy under simulated demand elasticity?
4. **HOW MUCH?** What are projected unit economics, gross margins, delivery costs, and operating revenues?
5. **WHEN?** Under what operational horizon does the new market entry achieve break-even?
6. **WHAT IF?** How resilient is the business model against macro cost shocks and competitive pressure?
7. **WHY?** What is the structured, defensible business rationale explaining the algorithm's decisions?

---

## 2. End-to-End Decision Architecture

```text
                                 MARKETPULSE ENGINE
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │     Market Research & Data Ingestion  │
                     │   (Census, MoSPI, Competitor Density) │
                     └───────────────────┬───────────────────┘
                                         ↓
                     ┌───────────────────────────────────────┐
                     │       PostgreSQL Data Warehouse       │
                     │     (Relational Analytics Schema)     │
                     └───────────────────┬───────────────────┘
                                         ↓
                     ┌───────────────────────────────────────┐
                     │       Core Analytics & Profiling      │
                     │  (EDA, RFM Segmentation, Cohorts)    │
                     └───────────────────┬───────────────────┘
                                         ↓
                 ┌───────────────────────┼───────────────────────┐
                 ↓                       ↓                       ↓
      ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
      │   MCDA City Scoring │ │   Scenario & Pricing│ │ Bottom-Up TAM Sizing│
      │  (Weighted Ranking) │ │ Sensitivity Engine  │ │  (Demographic Model)│
      └──────────┬──────────┘ └──────────┬──────────┘ └──────────┬──────────┘
                 └───────────────────────┼───────────────────────┘
                                         ↓
                     ┌───────────────────────────────────────┐
                     │     AI Strategic Explanation Layer    │
                     │   (Deterministic Narrative Synthesis) │
                     └───────────────────┬───────────────────┘
                                         ↓
                     ┌───────────────────────────────────────┐
                     │  Interactive Streamlit Decision Desk  │
                     │      (Executive KPI Dashboards)       │
                     └───────────────────┬───────────────────┘
                                         ↓
                                STRATEGIC DIRECTIVE
```

---

## 3. Key Findings & Empirical Benchmark Results

| Decision Dimension | Quantitative Finding | Strategic Context & Management Action |
| :--- | :--- | :--- |
| **Recommended City** | **Bengaluru (Score: 77.50/100.0)** | #1 in internet penetration (75.0%), digital adoption (22.0%), and purchasing power. |
| **Runner-Up Market** | Delhi NCR (Score: 65.57/100.0) | High aggregate market size, but elevated dark-store competitive saturation. |
| **Bottom-Up City TAM** | **INR 194.91 Crores (~INR 1.95B)** | Derived across 180,468 active eCommerce households in Bengaluru. |
| **National Category TAM** | **INR 1,200 Crores** | Reference market baseline across 5 Tier-1 metropolitan hubs. |
| **Key Profit Segment** | **Frequent Segment** | Represents 25% of active users but generates **45.2% of total margin**. |
| **Recommended Pricing** | **Medium (Competitive Parity)** | Maximizes contribution margin while maintaining high order velocity. |
| **Projected Break-Even** | **Month 18 (Base Case)** | Achieved under disciplined CAC (<= INR 300) and delivery route consolidation. |
| **Critical Risk Trigger** | **CAC > INR 350 / User** | CAC expansion above INR 350 delays unit break-even beyond Month 22. |

---

## 4. Quickstart & Installation

### Option A: Local Python Environment
```bash
# 1. Clone repository
git clone https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine.git
cd MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine

# 2. Install pinned dependencies
pip install -r requirements.lock.txt

# 3. Execute headless decision pipeline (generates benchmark artifacts)
python run_pipeline.py --seed 42 --benchmark

# 4. Launch interactive dashboard
streamlit run src/dashboard/app.py
```

### Option B: Docker Compose (Isolated Environment)
```bash
# Build and orchestrate PostgreSQL + Analytics Pipeline + Streamlit Dashboard
docker compose up --build
```
Access the interactive dashboard at `http://localhost:8501`.

---

## 5. Testing, Quality Assurance & Security Gates

The repository maintains an **80%+ test coverage gate** enforced via GitHub Actions CI:

```bash
# Execute Pytest test suite with coverage enforcement
python -m pytest tests/ -v --cov=src --cov-fail-under=80

# Verify code formatting and linting
black --check src/ tests/ run_pipeline.py
isort --check-only src/ tests/ run_pipeline.py
flake8 src/ tests/ run_pipeline.py

# Static type checking
python -m mypy --explicit-package-bases src/ tests/ run_pipeline.py

# Static application security testing (AST)
bandit -r src/ -s B101,B311,B110
```

---

## 6. Repository Architecture

```text
MarketPulse/
├── .devcontainer/          # VS Code DevContainer development environment
├── .github/
│   ├── workflows/          # Ultra-fast GitHub Actions CI/CD and Docker pipelines
│   └── dependabot.yml      # Automated dependency vulnerability scanning
├── configs/                # Centralized YAML configuration files (default.yaml)
├── data/
│   ├── raw/                # Public demographic reference data (MoSPI, Census)
│   ├── processed/          # Cleaned city market & competitor metrics
│   ├── synthetic/          # Causally linked transaction datasets
│   └── benchmarks/         # Exported model evaluation artifacts (.json, .csv)
├── database/
│   ├── queries/            # Business SQL analytics scripts (01 to 06)
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
├── tests/                  # Pytest test suite (31 tests, 87.63% coverage)
├── .env.example            # Sample production environment variables
├── .flake8                 # Flake8 style configuration
├── .gitattributes          # Cross-platform LF line-ending normalization
├── .gitignore              # Standard git exclusion rules
├── CHANGELOG.md            # Release version history
├── CONTRIBUTING.md         # Developer contribution guidelines
├── Dockerfile              # Production multi-stage container definition
├── docker-compose.yml      # Multi-container orchestration
├── pyproject.toml          # Unified project & tooling configuration
├── requirements.txt        # Runtime and development dependency declarations
├── requirements.lock.txt   # Pinned dependency lockfile
├── run_pipeline.py         # Headless CLI pipeline runner
└── SECURITY.md             # Security policy and threat modeling
```

---

## 7. License

This project is licensed under the [MIT License](LICENSE).
