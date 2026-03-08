# MachineACS

**Deterministic, auditable data cleaning infrastructure.**

Most data cleaning tools are built on statistical inference. They estimate. They suggest. They approximate. When you ask why a record was changed, they give you a confidence score.

MachineACS is built on a different premise: that data correctness should be provable, not probable. Every transformation is deterministic, every decision is traceable, and the same input will always produce the same output — on any machine, at any time.

---

## The Thesis

The data quality industry has a structural problem. Probabilistic systems can detect that something looks wrong. They cannot guarantee that anything is right.

This distinction matters more every year. Regulated industries — finance, healthcare, legal — are being asked to demonstrate that the data feeding their AI systems is valid. Not "probably valid." Valid. With an audit trail that survives a regulator's question.

The tools that exist today cannot answer that question. They were not built to. MachineACS is.

---

## How It Works

MachineACS enforces data quality through three architectural layers, each building on the last.

**Canonicalization** takes dirty, ambiguous input and collapses it into a single deterministic canonical form. The same data — regardless of encoding variation, key insertion order, type inconsistency, or Unicode normalization — always produces the same bytes and the same hash. This is the foundation everything else depends on. Without it, identity is unstable and the audit trail is meaningless.

**Semantic Entity Resolution** identifies records that refer to the same real-world entity despite surface-level variation. "Jon Smith" and "John Smith", "IBM Corp" and "IBM Corporation" — these are the same entity. Resolution combines string distance metrics, phonetic matching, and graph-based clustering to group records at scale, without the O(N²) complexity of naive comparison.

**The Causal Constraint Engine (CCE)** is the core architectural innovation. It encodes domain knowledge as a causal directed acyclic graph — a formal model of which fields causally influence which other fields. When a record is cleaned and a field changes upstream (e.g. Job Title), the CCE automatically propagates validation obligations to every causally dependent field downstream (e.g. Salary, Department). Constraints are expressed in a Datalog-style rule language and enforced deterministically. Not estimated. Enforced.

Every transformation produces a before-hash and after-hash stored in an immutable audit log. The chain is queryable and replayable. You can prove what happened to any record at any point in the pipeline.

This is the git model applied to data.

---

## Roadmap

| Stage | What Gets Built | Status |
|---|---|---|
| 0 — Foundations | Python basics, single-file text cleaner | ✅ Complete |
| 1 — Deep Python | Multi-file architecture, modules, imports, pytest | ✅ Complete |
| 2 — Data Engineer | CSV/JSONL/JSON streaming pipeline, generators, OOP | ✅ Complete |
| 2.5 — Production Standards | uv dependency management, mypy typing, multiprocessing | ✅ Complete |
| 3 — Backend Engineer | FastAPI server, PostgreSQL, async I/O, job system | ✅ Complete |
| 4 — Deterministic Foundations | Canonicalization, stable hashing, content-addressed identity, audit log | ✅ Complete |
| **5 — Entity Resolution Primitives** | **Levenshtein distance, Jaccard similarity, naive O(N²) deduplication** | 🔧 In Progress |
| 6 — Graph Data Structures | Union-Find, adjacency lists, connected components clustering | Planned |
| 7 — Logic & AST Foundations | Safe rule engine, AST traversal, Datalog-style constraints | Planned |
| 8 — Advanced Entity Resolution | Phonetic blocking (Double Metaphone), golden record selection | Planned |
| 9 — Network Dynamics | Community detection, weakly connected components, clique analysis | Planned |
| 10 — Causal Intelligence | DAG-based validation, intervention propagation, counterfactual reasoning | Planned |
| 11 — Semantic Architecture | Headless metric layer, API-first constraint definitions | Planned |

The roadmap is intentionally sequential. Each stage is a prerequisite for the next. Stage 10 — the CCE — is the commercial core. Everything before it is engineering toward that moment.

---

## What Stage 4 Established

Stage 4 is the most important completed milestone because it proves the core premise is buildable. The deterministic foundation is not theoretical — it is implemented and tested against real dirty HR data with 200 records, 30 duplicate pairs, and every class of real-world dirty variation.

The key guarantee: given any two records that represent the same real-world entity, after canonicalization they produce the same hash. This holds across mixed types (`32` vs `"32"` vs `32.0`), Unicode encoding variants (NFC vs NFD decomposition), null representations (`""`, `"N/A"`, `null`, `None`), float arithmetic noise, and arbitrary key insertion order.

The audit log stores `(before_hash, rules_applied, after_hash)` for every record. Records where `before_hash == after_hash` are explicit proof of validity — not silence. The full transformation chain is queryable.

---

## Repository Structure

```
machineacs/
├── adapters/
│   ├── canonicalizer.py        # SHA-256 content-addressed identity
│   └── format.py               # File type yielders (CSV, JSON, JSONL, TXT)
├── filters/
│   ├── tokens.py               # Token hierarchy (Hash, Rule, Key, Value, Structural)
│   ├── json_structurer.py      # Streaming JSON/JSONL token pipeline
│   ├── schema_coercer.py       # Key standardization + type coercion + rule emission
│   ├── whitespace.py
│   ├── regex.py
│   └── grammar.py
├── config/
│   ├── registry.py             # Filter registry and pipeline orchestration
│   └── settings.json
├── utils/
│   ├── io.py                   # Async file writer
│   ├── logger.py
│   └── paths.py
├── tests/
│   ├── generate_hr_data.py     # Dirty HR test data generator (200 records, 30 duplicate pairs)
│   ├── test_filters.py
│   └── test_adapters.py
└── the cool files/             # FastAPI server, PostgreSQL integration, job system
    ├── api.py
    ├── cleaner.py
    └── database.py
```

---

## Setup

**Requirements:** Python 3.12+, PostgreSQL

```bash
git clone https://github.com/hamzasedrati/machineacs
cd machineacs

# Install with uv
uv sync

# Generate test data
python tests/generate_hr_data.py

# Run the API server
uvicorn "the cool files/api:app" --reload

# Run tests
pytest tests/
```

---

## The Larger Vision

MachineACS is the first product of Sedrati, a technology company targeting the 2027–2030 window when enterprise AI governance regulation creates structural demand for deterministic verification infrastructure.

The incumbents in data quality — Monte Carlo, Soda, Anomalo — are built entirely on statistical inference. Rewriting them to support symbolic constraint enforcement requires starting over architecturally. They cannot get there from where they are. MachineACS is being built from the right foundation.

---

## Background Reading

- Pearl — *Causality: Models, Reasoning, and Inference* (2000)
- Rekatsinas et al. — *HoloClean: Holistic Data Repairs with Integrity Constraints* (2017)
- Peters, Janzing, Schölkopf — *Elements of Causal Inference* (2017)

---

*Built by Hamza Sedrati. Sec 5, Quebec. Stage 5 in progress.*
