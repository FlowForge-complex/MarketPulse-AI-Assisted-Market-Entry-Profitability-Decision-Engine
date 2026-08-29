# Contributing to MarketPulse

Thank you for your interest in contributing to **MarketPulse: AI-Assisted Market Entry & Profitability Decision Engine**! This guide outlines the development environment setup, coding conventions, testing requirements, and pull request workflow.

---

## 1. Development Setup

### Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Git
- Optional: Docker & Docker Compose

### Local Installation
```bash
# 1. Clone the repository
git clone https://github.com/Vineesh-12/MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine.git
cd MarketPulse-AI-Assisted-Market-Entry-Profitability-Decision-Engine

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# 3. Install pinned dependencies including development tools
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Coding Standards & Tooling

All code committed to MarketPulse must pass automated formatting, linting, type-checking, and security audits.

### Code Formatting & Imports
We use `black` and `isort`:
```bash
black src/ tests/
isort src/ tests/
```

### Style Linting
We use `flake8`:
```bash
flake8 src/ tests/
```

### Static Type Checking
We use `mypy`:
```bash
mypy src/ tests/
```

### Security Scanning
We use `bandit` and `pip-audit`:
```bash
bandit -r src/
pip-audit -r requirements.txt
```

---

## 3. Testing Guidelines

We enforce a strict **80%+ test coverage threshold** across all source code.

- Always pair new features or bug fixes with comprehensive unit tests under `tests/`.
- Ensure tests verify numeric behavior, input validation exceptions, and boundary conditions.
- Run the full test suite locally before pushing:
```bash
python -m pytest tests/ -v --cov=src --cov-fail-under=80
```

---

## 4. End-to-End Verification

Before submitting a Pull Request, verify that the headless pipeline runner executes with exit code 0:
```bash
python run_pipeline.py --seed 42 --benchmark
```

---

## 5. Pull Request Workflow

1. **Create a branch:** Use semantic branch naming (e.g., `feat/add-new-metric`, `fix/scoring-weight-tolerance`).
2. **Atomic Commits:** Structure commits into focused, single-purpose changes paired with their tests.
3. **Semantic Messages:** Use Conventional Commits (`feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `refactor: ...`).
4. **CI Green:** Ensure all GitHub Actions matrix jobs pass.
