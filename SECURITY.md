# Security Policy & Formal Threat Model

## 1. Executive Threat Model

MarketPulse operates as an analytical decision-support engine. This threat model formally defines the security architecture, asset classifications, trust boundaries, threat vectors, and automated defense controls.

### 1.1 Asset Classifications
1. **API Keys & Credentials:** `GEMINI_API_KEY`, `OPENAI_API_KEY`, and PostgreSQL database connection strings (`DATABASE_URL`).
2. **Analytical Data Assets:** Processed market metrics (`data/processed/`), transaction ledgers (`data/synthetic/`), and exported benchmark evaluations (`data/benchmarks/`).
3. **Deterministic Decision Models:** Multi-Criteria Decision Analysis (MCDA) algorithms, pricing elasticity matrices, and bottom-up TAM formulas.
4. **AI Narrative Synthesis:** Structured metric payloads and explanation prompt templates.

### 1.2 Trust Boundaries & Data Flow Architecture
```text
  [ External User / Client ]
             │
   (Trust Boundary 1: Web Interface / CLI)
             ▼
  [ Streamlit UI / CLI Runner ] ──► [ Secret Redaction Logging Filter ]
             │
   (Trust Boundary 2: Ingestion & Parsing)
             ▼
  [ Pydantic Ingestion Schemas ] ──► [ Validated DataFrames ]
             │
   (Trust Boundary 3: Model Execution)
             ▼
  [ MCDA & TAM Analytical Engine ]
             │
   (Trust Boundary 4: AI Explanation Layer)
             ▼
  [ Deterministic Fallback / LLM Prompt ] ──► [ Final Decision Output ]
```

### 1.3 Threat Vectors & Defense Mitigations
| Threat Vector | Risk Classification | Defense Mechanism & Controls |
| :--- | :---: | :--- |
| **Credential & Key Leakage in Logs** | **CRITICAL** | Automated `SecretRedactionFilter` regex stream scanner masking API keys and tokens with `[REDACTED]`. |
| **Data Ingestion Schema Poisoning** | **HIGH** | Pydantic boundary models (`CityMetricsSchema`, `OrderIngestSchema`, etc.) enforcing typed constraints and raising `DataLoadError` on violation. |
| **Prompt Injection & Fabricated Output** | **HIGH** | Strict separation of data payload from prompt templates; deterministic offline narrative fallback when API keys are absent. |
| **SQL Injection in Data Warehouse** | **HIGH** | Parameterized query abstractions in PostgreSQL analytics scripts (`database/queries/`). |
| **Container Privilege Escalation** | **MEDIUM** | Multi-stage `Dockerfile` executing under unprivileged `appuser` (UID 1000) with non-root runtime permissions. |
| **Dependency Vulnerabilities (CVEs)** | **MEDIUM** | AST scanning via `bandit`, dependency vulnerability auditing with `pip-audit`, and automated PR updates with Dependabot. |

---

## 2. Secrets Management & Keyless Isolation

* **Zero Hardcoded Secrets:** No API keys, credentials, or production tokens may be committed to version control. Verified via automated pre-commit scanners (`bandit` and AST checks).
* **Keyless Full-Isolation Execution:** The entire analytics pipeline and AI explanation layer operate 100% offline without requiring external API keys. When `GEMINI_API_KEY` / `OPENAI_API_KEY` are unset, the system executes deterministic narrative synthesis.
* **Environment Configuration:** All optional credentials are read strictly via environment variables declared in [`.env.example`](.env.example).

---

## 3. Supported Versions & Patch Policy

| Version | Supported | Security Update Cadence |
| :--- | :---: | :--- |
| **1.1.x** | :white_check_mark: | Active support; critical patches released within 48 hours. |
| **1.0.x** | :x: | End of Life (Deprecated). |

---

## 4. Reporting a Vulnerability

If you discover a security vulnerability, please submit a responsible disclosure report:

1. **Email:** `security@marketpulse-engine.org` or open a private GitHub Security Advisory.
2. **Report Contents:**
   - Vulnerability description, affected module, and reproduction steps.
   - Proof-of-concept (PoC) code demonstrating the issue.
   - Assessment of potential impact on confidentiality, integrity, or availability.
3. **Response SLA:**
   - **Triage & Acknowledgement:** Within 24–48 hours.
   - **Remediation & Patch Release:** Within 7 business days.
