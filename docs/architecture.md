# PaperPilot Pro Architecture

## Overview

PaperPilot Pro uses a React frontend and a FastAPI backend. The backend coordinates document ingestion, retrieval, generation, citation validation, and evaluation.

## Request Flow

1. A user uploads a research PDF.
2. The backend extracts page-level text.
3. Text is divided into chunks with stable identifiers and page metadata.
4. An embedding provider generates vectors.
5. Chunks and metadata are stored in PostgreSQL with pgvector.
6. A question triggers semantic and keyword retrieval.
7. A reranker selects the most relevant evidence.
8. A configurable LLM generates an answer using that evidence.
9. Citation validation checks references against retrieved chunks.
10. The API returns the answer, citations, and diagnostic metadata.

## Provider Independence

Generation and embedding providers will use separate interfaces. Switching the generation model must not require rewriting retrieval or API routes.

## Reliability

The system will validate uploads, handle provider failures, track request latency, test unsupported questions, and avoid treating uploaded document instructions as trusted system instructions.

## Initial Scope

Single-user research workspace, PDF ingestion, multi-document RAG, citations, hosted/local model selection, and offline evaluation.