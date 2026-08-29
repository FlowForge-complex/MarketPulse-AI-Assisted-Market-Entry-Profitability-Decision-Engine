# Security Policy & Threat Model

## 1. Threat Model Overview

MarketPulse is a deterministic analytics and decision engine. The threat modeling encompasses data integrity, configuration poisoning, SQL injection prevention, and LLM prompt injection safeguards.

### Core Assets & Trust Boundaries
1. **Raw & Processed Data Integrity:** City demographics and transaction records must be validated against expected schema boundaries.
2. **Deterministic Computation Layer:** The decision engine and scoring algorithms must execute without non-deterministic side-effects or unauthorized weight mutations.
3. **AI Explanation Layer:** LLM prompts are isolated so that external data cannot override decision rules or hallucinate fabricated metrics.
4. **Database & Secrets:** No credentials or API keys may be committed to version control.

### Mitigation Strategies
| Threat Vector | Risk Level | Mitigation Strategy |
| :--- | :--- | :--- |
| Schema / Data Poisoning | Medium | Strict validation using typed dataclasses (`src/core/types.py`) and schema checks. |
| SQL Injection | High | Parameterized queries and ORM abstractions in PostgreSQL database layer. |
| Non-deterministic Execution | Medium | Fixed global random seeds (`--seed 42`) across all stochastic generators. |
| Prompt Injection / Hallucination | High | Structured JSON payload ingestion with deterministic markdown templating. |
| Vulnerable Dependencies | Medium | Automated dependency scanning using `pip-audit`, `bandit`, and Dependabot. |

---

## 2. Supported Versions

Security updates and patches are actively maintained for the following versions:

| Version | Supported |
| :--- | :--- |
| 1.1.x | :white_check_mark: |
| 1.0.x | :x: |

---

## 3. Reporting a Vulnerability

We take the security of MarketPulse seriously. If you discover a potential security vulnerability, please report it responsibly:

1. **Email:** Send details of the vulnerability to `security@marketpulse-engine.org` (or create a private GitHub Security Advisory).
2. **Details to Include:**
   - Description of the vulnerability and affected components.
   - Step-by-step reproduction instructions or proof of concept.
   - Impact assessment on data integrity or pipeline execution.
3. **Response Timeline:**
   - Initial acknowledgement within 48 hours.
   - Triage and mitigation patch released within 7 business days.

Please do **not** disclose security vulnerabilities publicly until a patch has been released.
