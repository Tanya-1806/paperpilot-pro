# Decision 001: Vector Storage

## Status

Proposed.

## Context

PaperPilot Pro requires vector similarity search and persistent document metadata. The initial project must remain manageable for a single developer.

## Decision

Use PostgreSQL with pgvector for the initial implementation.

## Rationale

- Store document metadata and embeddings in one database.
- Reduce infrastructure complexity.
- Support vector similarity search alongside ordinary relational queries.
- Keep local development reproducible with Docker Compose.

## Trade-offs

A dedicated vector database may offer advantages for larger workloads or specialized retrieval requirements. PostgreSQL with pgvector is the initial choice for simplicity, not a claim that it is universally superior.

## Revisit When

Benchmark results or workload requirements demonstrate that the current database is a bottleneck.