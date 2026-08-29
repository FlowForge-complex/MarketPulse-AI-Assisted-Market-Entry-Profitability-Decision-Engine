# Changelog

All notable changes to the **MarketPulse** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-08-29

### Added
- **Core Architecture:** Introduced structured logging framework (`src/core/logging_config.py`) with JSON and human-readable formatting.
- **Strict Typing:** Added typed dataclasses and custom validation exceptions (`src/core/types.py`).
- **CLI Pipeline Runner:** Added `run_pipeline.py` with reproducible seed control, headless execution, and benchmark artifact exports.
- **Testing Suite:** Expanded test suite across all analytical and decision modules, enforcing an 80%+ coverage gate (`pytest-cov`).
- **Containerization:** Added production `Dockerfile`, `docker-compose.yml` multi-service orchestration, and `.devcontainer/devcontainer.json`.
- **Quality & Security Tooling:** Configured `pyproject.toml`, `.flake8`, `bandit`, `pip-audit`, `black`, `isort`, and `mypy`.
- **Pinned Dependencies:** Added `requirements.lock.txt` for exact dependency reproducibility.
- **Governance:** Added `SECURITY.md`, `CONTRIBUTING.md`, and automated Dependabot configuration.

### Changed
- Refactored `eda.py`, `rfm.py`, `retention.py`, and `profitability.py` to utilize structured logging and typed interfaces.
- Upgraded city scoring and sensitivity engines with strict Multi-Criteria Decision Analysis (MCDA) weight validation.
- Streamlined Streamlit dashboard UI and embedded executive artifacts into `README.md`.

## [1.0.0] - 2026-08-24

### Added
- Initial project scaffolding and folder structure.
- Phase 1 market research datasets and synthetic transaction generators.
- PostgreSQL relational schema and analytical business queries.
- Python-based exploratory data analysis and RFM segmentation.
- Multi-criteria city attractiveness decision engine.
- Bottom-up Total Addressable Market (TAM) guesstimation engine.
- AI Explanation Layer with deterministic prompt guardrails.
- Financial model workbook structure and 12-slide executive consulting deck.
- Interactive Streamlit executive web dashboard.
