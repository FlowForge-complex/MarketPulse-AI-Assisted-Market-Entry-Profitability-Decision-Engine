# Security Policy, Threat Model & Secrets Management

## 1. Executive Threat Model

MarketPulse operates as an analytical decision-support engine. This threat model formally defines the security architecture, asset classifications, trust boundaries, threat vectors, key rotation policies, automated defense controls, and residual risks.

### 1.1 Asset Classifications & Impact of Potential Leaks
1. **AI Provider API Keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`):**
   * *Risk:* Unauthorized LLM API consumption and quota exhaustion.
   * *Mitigation:* The system operates 100% offline via deterministic narrative synthesis when keys are unset. Keys are ingested via `SecretsManager` and masked in logs.
2. **Database Credentials (`DATABASE_URL`):**
   * *Risk:* Unauthorized access to PostgreSQL analytical schemas and data tables.
   * *Mitigation:* Parameterized SQL abstractions, non-root database container permissions, and network-isolated Docker networks.
3. **Analytical Data & Benchmark Assets:**
   * *Risk:* Schema poisoning or data corruption.
   * *Mitigation:* Pydantic boundary validation (`CityMetricsSchema`, `OrderIngestSchema`) rejecting malformed inputs with `DataLoadError`.
4. **Deterministic Decision Models & DAG Pipeline:**
   * *Risk:* Non-deterministic calculation drift.
   * *Mitigation:* Global random seeds (`--seed 42`) and SHA-256 evaluation checksum verification.

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
   (Trust Boundary 3: Directed Acyclic Graph Orchestration)
             ▼
  [ DAG Task Engine (EDA -> Scoring -> TAM -> Ablation) ]
             │
   (Trust Boundary 4: AI Explanation Layer)
             ▼
  [ Deterministic Offline Fallback / LLM Synth ] ──► [ Final Decision Output ]
```

### 1.3 Threat Vectors & Defense Mitigations
| Threat Vector | Risk Classification | Defense Mechanism & Controls |
| :--- | :---: | :--- |
| **Credential & Key Leakage in Logs** | **CRITICAL** | Automated `SecretRedactionFilter` regex stream scanner masking API keys and tokens with `[REDACTED]`. |
| **Data Ingestion Schema Poisoning** | **HIGH** | Pydantic boundary models (`CityMetricsSchema`, `OrderIngestSchema`, etc.) enforcing typed constraints and raising `DataLoadError` on violation. |
| **Prompt Injection & Fabricated Output** | **HIGH** | Strict separation of data payload from prompt templates; deterministic offline narrative fallback when API keys are absent. |
| **SQL Injection in Data Warehouse** | **HIGH** | Parameterized query abstractions in PostgreSQL analytics scripts (`database/queries/`). |
| **Container Privilege Escalation** | **MEDIUM** | Multi-stage `Dockerfile` executing under unprivileged `appuser` (UID 1000) with non-root runtime permissions. |
| **Dependency Vulnerabilities (CVEs)** | **MEDIUM** | AST scanning via `bandit`, strict dependency auditing with `pip-audit`, and automated PR updates with Dependabot. |

---

## 2. Secrets Management & Vault Integration

MarketPulse provides a provider-agnostic `SecretsManager` (`src/core/secrets_manager.py`) supporting multiple backends:

1. **Environment Variables (`EnvSecretsProvider`):** Default for development and local testing.
2. **Vault / Cloud Secrets (`VaultSecretsProvider`):** Integration for production deployments using HashiCorp Vault or AWS Secrets Manager with in-memory caching and rotation.

### Production Secret Manager Configuration
To swap `.env` for a secret manager in production:
```python
from src.core.secrets_manager import VaultSecretsProvider, get_secrets_manager

vault_provider = VaultSecretsProvider({
    "GEMINI_API_KEY": "<vault_fetched_key>",
    "DATABASE_URL": "<vault_fetched_db_url>",
})
get_secrets_manager().set_provider(vault_provider)
```

### Key Rotation SLA
* **Standard Key Rotation:** Every 90 days across all cloud provider keys and database credentials.
* **Emergency Revocation SLA:** Revocation and secret rotation completed within 4 hours of confirmed compromise.

### Secret Redaction Filter Coverage
The `SecretRedactionFilter` in `src/core/logging_config.py` actively intercepts:
* Google Gemini API Keys (`AIzaSy[A-Za-z0-9_-]{33}`)
* OpenAI API Keys (`sk-[A-Za-z0-9-_]{20,}`)
* GitHub Personal Access Tokens (`ghp_[A-Za-z0-9]{36}`)
* Authorization Bearer Headers (`Bearer\s+[A-Za-z0-9\-._~+/]+=*`)

---

## 3. Known Residual Risks & Assessment

| Residual Risk Vector | Impact Severity | Operational Context & Buyer Assessment |
| :--- | :---: | :--- |
| **Transitive Dependency Drift** | Low | `pip-audit` scans direct and pinned lockfile dependencies. Sub-dependencies without published CVEs remain subject to future upstream disclosure. |
| **In-Memory Secret Lifetime** | Low | Process memory dumps on compromised host environments could reveal active runtime tokens prior to garbage collection. Mitigated by OS-level container isolation. |
| **Offline Model Heuristic Divergence** | Low | Offline narrative generation relies on structured metrics templates rather than dynamic LLM inference, ensuring complete data containment at the cost of subjective nuance. |

---

## 4. Supported Versions & Patch Policy

| Version | Supported | Security Update Cadence |
| :--- | :---: | :--- |
| **1.1.x / 1.2.x** | :white_check_mark: | Active support; critical patches released within 48 hours. |
| **1.0.x** | :x: | End of Life (Deprecated). |

---

## 5. Reporting a Vulnerability

If you discover a security vulnerability, please submit a responsible disclosure report:

1. **Email:** `security@marketpulse-engine.org` or open a private GitHub Security Advisory.
2. **Report Contents:**
   - Vulnerability description, affected module, and reproduction steps.
   - Proof-of-concept (PoC) code demonstrating the issue.
   - Assessment of potential impact on confidentiality, integrity, or availability.
3. **Response SLA:**
   - **Triage & Acknowledgement:** Within 24–48 hours.
   - **Remediation & Patch Release:** Within 7 business days.
