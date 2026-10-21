# PaperPilot Pro

**An evidence-grounded AI research copilot for multi-document analysis.**

PaperPilot Pro is a full-stack Generative AI application designed to help users explore research papers, compare findings, and obtain answers supported by verifiable source citations.

## Problem Statement

Reading multiple research papers and locating evidence across them is time-consuming. Conventional AI-generated summaries can also contain unsupported claims or unreliable citations.

PaperPilot Pro aims to make research more efficient by combining retrieval-augmented generation (RAG), document-level evidence tracking, and systematic evaluation.

## Planned Features

- PDF ingestion with page-level metadata
- Semantic and keyword-based document retrieval
- Cross-encoder reranking
- Evidence-grounded question answering
- Source-linked citations and evidence-based abstention
- Hosted and locally served LLM support
- Research paper comparison
- Automated retrieval and answer evaluation
- Interactive React frontend and FastAPI backend

## Technology Stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **Backend:** Python, FastAPI, Pydantic
- **Database:** PostgreSQL, SQLAlchemy, Alembic, pgvector
- **AI:** Sentence Transformers, configurable LLM providers
- **Testing:** pytest, HTTPX, Vitest, Playwright
- **Development:** Docker Compose, GitHub Actions

## Project Status

Day 1 — Requirements, repository setup, and architecture planning.

## Evaluation

The project will be evaluated using a curated research-question dataset, retrieval metrics, answer correctness, citation validity, faithfulness, latency, and estimated inference cost.

## Engineering Principles

- Evidence before confident answers
- Reproducible experiments
- Automated testing
- Transparent limitations
- Secure handling of uploaded documents

## License

To be determined before the first public release.