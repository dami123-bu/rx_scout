# RxSCOUT

### Repurposing × Systematic Candidate Output Using Transformers

An agentic RAG system that discovers drug repurposing opportunities. Given an existing approved drug, RxSCOUT deploys specialized ReAct agents that reason across biomedical literature, structured drug databases, and clinical trial registries to identify and rank new therapeutic indications.

---

## Overview

Drug development takes 10–15 years and costs over $2 billion per approved therapy. Drug repurposing — finding new indications for existing approved drugs — dramatically reduces this timeline. RxSCOUT automates the discovery process, enabling researchers to generate structured, evidence-backed repurposing hypotheses in minutes rather than weeks.

**Input:** A drug name (e.g., "Metformin")

**Output:** A ranked report of candidate diseases with discovery paths, literature evidence summaries, clinical trial status, and novelty scores.

---

## Architecture

```
User Input: "Find repurposing opportunities for [Drug X]"
                          │
                          ▼
              ┌───────────────────────┐
              │   Orchestrator Agent  │
              │      (ReAct Loop)     │
              └───────┬───────────────┘
                      │
         ┌────────────┼────────────┬──────────────┐
         ▼            ▼            ▼              ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
   │  Drug     │ │Literature│ │ Clinical │ │  Repurposing │
   │  Profile  │ │  Agent   │ │  Trial   │ │  Discovery   │
   │  Agent    │ │  (RAG)   │ │  Agent   │ │  Agent       │
   └──────────┘ └──────────┘ └──────────┘ └──────────────┘
       │             │            │               │
       ▼             ▼            ▼               ▼
   DrugBank      PubMed       ClinicalTrials   Multi-relational
                Vector Store   .gov API         knowledge base
```

### Agents

| Agent | Role | Data Sources |
|-------|------|-------------|
| **Drug Profile** | Retrieves and structures comprehensive drug information | DrugBank |
| **Repurposing Discovery** | Explores multiple relationship types to surface candidate diseases | PostgreSQL knowledge base |
| **Literature** | RAG-based evidence retrieval and synthesis for each drug-disease pair | PubMed via pgvector |
| **Clinical Trial** | Validates novelty and checks trial landscape | ClinicalTrials.gov API |

### Discovery Paths

The Repurposing Discovery Agent explores candidates through five strategies:

1. **Phenotypic similarity** — diseases sharing features with current indications
2. **Side effect signal analysis** — side effects as indicators of therapeutic potential
3. **Drug class analogy** — indications treated by drugs in the same pharmacological class
4. **Comorbidity patterns** — co-occurring diseases that may share addressable biology
5. **Mechanism extrapolation** — diseases where the drug's known mechanisms are implicated

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent framework | LangGraph |
| LLM | Claude (Anthropic API) |
| Embeddings | PubMedBERT |
| Vector store | pgvector (PostgreSQL 16) |
| Knowledge base | PostgreSQL 16 |
| Clinical trials | ClinicalTrials.gov API |
| UI | Streamlit |
| Language | Python 3.11+ |

---

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Anthropic API key

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/rxscout.git
cd rxscout
```

### 2. Install dependencies

```bash
pip install -e ".[dev]"
```

### 3. Configure environment

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your-key-here
```

### 4. Start the database

```yaml
# docker-compose.yml
services:
  db:
    image: pgvector/pgvector:pg16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: rxscout
      POSTGRES_USER: rxscout
      POSTGRES_PASSWORD: rxscout_dev
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
docker compose up -d
```

This starts PostgreSQL 16 with pgvector on port 5432. Data is persisted in a named volume.

### 5. Ingest data

```bash
make ingest
```

### 6. Build vector index

```bash
make index
```

---

## Usage

### Streamlit UI

```bash
make run
```

### Running tests

```bash
# Unit tests only
pytest -m "not integration"

# All tests (requires database and API access)
pytest
```

---

## Project Structure

```
rxscout/
├── src/rxscout/
│   ├── agents/           # ReAct agents (orchestrator, drug profile, discovery, literature, clinical trial)
│   ├── rag/              # Embedding, indexing, and retrieval pipeline
│   ├── db/               # Database schema, connection, migrations
│   ├── data/ingest/      # Data ingestion scripts (PubMed, DrugBank, SIDER)
│   ├── eval/             # Evaluation framework and ground truth
│   └── ui/               # Streamlit interface
├── tests/
├── docs/                 # Project documentation and technical plans
├── pyproject.toml
├── docker-compose.yml
└── Makefile
```

---

## Evaluation

RxSCOUT is evaluated against a ground truth dataset of known successful drug repurposings (e.g., Thalidomide → multiple myeloma, Sildenafil → pulmonary hypertension).

| Metric | Description |
|--------|-------------|
| Recall@K | Does the known repurposed indication appear in the top K candidates? |
| MRR | Mean Reciprocal Rank — how highly is the correct indication ranked? |
| Evidence quality | Human evaluation of evidence summary accuracy and sourcing |

Baselines: naive RAG (no agents) and single-path discovery (mechanism only).

---

## License

MIT — see [LICENSE](LICENSE) for details.