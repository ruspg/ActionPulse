# ActionPulse

Daily corporate communications digest with LLM extraction. Privacy-first, evidence-traced.

## Repo Structure

```
digest-core/     # Python package — the actual product (see digest-core/AGENTS.md)
scripts/         # Installation and setup scripts (install.sh, setup.sh)
```

Monorepo with one package. All development happens in `digest-core/`.

## Root Shim (dev convenience only)

Two files at the repo root allow `python -m digest_core.cli` to be run **without** `cd digest-core`:

- **`sitecustomize.py`** — Python's auto-import hook; inserts `digest-core/src` into `sys.path` at interpreter startup.
- **`digest_core/__init__.py`** — Namespace package shim; extends `__path__` to the real package in `digest-core/src/digest_core/`.

**Canonical supported path:** `cd digest-core && python -m digest_core.cli …` (with `uv`-managed venv).

The root shim is a dev convenience and is **not** needed for Docker, systemd, or `pip install`. It may cause IDE confusion (two `digest_core` packages visible). Do not depend on it for production deployments.

## Key Documents

- `digest-core/docs/ARCHITECTURE.md` — **Single source of truth** for digest-core architecture, contracts, ADRs, roadmap (verify against code when in doubt)
- `digest-core/docs/PHASE0_PROMPT.md` — Historical Phase 0 execution checklist; not a guarantee that items are still open
- `docs/planning/BUSINESS_REQUIREMENTS.md` — Product / business requirements (repo root `docs/`)
- `docs/development/TECHNICAL.md` — Broader technical notes (may lag `digest-core`; prefer `ARCHITECTURE.md` for the Python package)

> **`Bus_Req_v5.md` / `Tech_details_v1.md`** are **not present** under `digest-core/docs/` in this repository (old references were stale).

## Language

- Code: English (variables, functions, comments)
- Output/prompts: Russian (дайджест is RU-first product)
- Docs: Russian for product docs, English for code-level docs

## Golden Rules

- Never log payloads or secrets. Structured logs only (structlog JSON).
- Every digest item MUST cite `evidence_id` and `source_ref` (principle P2: Traceability).
- Secrets via ENV only — never in YAML config files.
- Extract-over-Generate: LLM extracts from evidence, does not hallucinate (principle P1).
- Max 2 LLM calls per run (1 primary + 1 quality retry), each with 1 internal retry for transient errors. 15 RPM rate limit on qwen35-397b-a17b (ADR-008).

## Network Topology

- **EWS + LLM Gateway**: corp network only. Real tests only from inside.
- **Mattermost**: accessible from everywhere (delivery target).
- **Dev workflow**: "Code outside, run inside, debug outside" (ADR-012).
- Use `--dump-ingest` / `--replay-ingest` for offline development.
