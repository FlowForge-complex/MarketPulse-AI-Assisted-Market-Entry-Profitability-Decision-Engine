# Changelog

All notable changes to the **MarketPulse** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-09-01

### Added
- **DAG Pipeline Orchestrator:** Implemented topological graph execution engine (`src/pipeline/dag.py`) with per-task retry policies, task status telemetry, and dependency management.
- **Pipeline Idempotency:** Added SHA-256 evaluation metrics checksum verification guaranteeing deterministic outputs across repeated pipeline runs.
- **Provider-Agnostic Secrets Management:** Added `SecretsManager` (`src/core/secrets_manager.py`) supporting local `.env`, HashiCorp Vault, and AWS Secrets Manager with secret rotation simulation.
- **Service Health Probes:** Added `health_check()` endpoint (`src/core/health.py`) and wired healthcheck probes into `docker-compose.yml`.
- **Deterministic Tie-Breaking:** Added multi-criteria tie-break resolution hierarchy in `src/decision_engine/city_scoring.py`.
- **Strict CI Security Gate & Artifact Upload:** Enforced strict `pip-audit` gating and added `actions/upload-artifact@v4` in `.github/workflows/ci.yml`.
- **Pinned Lockfile:** Committed `requirements.lock` at repo root for zero-drift dependency resolution.
- **90% Coverage Enforcement:** Raised pytest coverage gate to `--cov-fail-under=90` (64 passing tests, 91.5% coverage).

### Changed
- Replaced imperative sequential execution in `run_pipeline.py` with Directed Acyclic Graph (DAG) task scheduling.
- Reconciled lockfile formats by standardizing on `requirements.lock` as the single source of truth.
- Enhanced `SECURITY.md` with residual risk matrices, rotation cadence SLAs, and redaction coverage patterns.

## [1.1.0] - 2026-08-29

### Added
- **Core Architecture:** Introduced structured logging framework (`src/core/logging_config.py`) with JSON and human-readable formatting.
- **Strict Typing:** Added typed dataclasses and custom validation exceptions (`src/core/types.py`).
- **CLI Pipeline Runner:** Added `run_pipeline.py` with reproducible seed control, headless execution, and benchmark artifact exports.
- **Testing Suite:** Expanded test suite across all analytical and decision modules, enforcing an 80%+ coverage gate (`pytest-cov`).
- **Containerization:** Added production `Dockerfile`, `docker-compose.yml` multi-service orchestration, and `.devcontainer/devcontainer.json`.
- **Quality & Security Tooling:** Configured `pyproject.toml`, `.flake8`, `bandit`, `pip-audit`, `black`, `isort`, and `mypy`.
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
