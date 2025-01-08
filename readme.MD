# Semantic Merkle Tree (SMT)

A novel data structure that combines semantic understanding with cryptographic hashing to create more resilient and intelligent file integrity verification.

## Overview

The Semantic Merkle Tree (SMT) enhances traditional Merkle Trees by incorporating semantic similarity detection before recalculating hashes. While classic Merkle Trees require complete hash recalculation when even minor changes occur (like adding a space or changing a single character), SMTs first evaluate if the changes meaningfully impact the content.

## Key Features

- **Semantic Change Detection**: Uses similarity engines to determine if content changes are significant enough to warrant hash updates
- **Reduced Hash Recalculations**: Only updates hashes when meaningful changes are detected
- **Flexible Similarity Methods**: Can utilize various approaches for semantic comparison:
  - BM25 scoring for keyword-based similarity (with configurable similarity threshold)
  - Hybrid search combining keywords and vectors
  - Embedding-based similarity using document vectors
  - Large Language Models for advanced semantic understanding

## How It Works

1. When a file change is detected, instead of immediately recalculating hashes, the SMT first analyzes the semantic similarity between the old and new versions
2. For traditional methods (BM25, embeddings):
   - A similarity threshold is configured (e.g., 95%)
   - If similarity score >= threshold, existing hashes are preserved
   - If similarity score < threshold, hashes are recalculated
3. For LLM-based comparison:
   - The LLM analyzes both versions and determines if semantic meaning has changed
   - Based on LLM's assessment, decides whether to preserve or recalculate hashes

## Implementation Note

While simpler similarity methods like BM25 (with configurable thresholds like 95%) or embedding-based comparisons could be used, this implementation leverages Large Language Models as they represent the cutting edge in semantic understanding. The LLM approach removes the need for manual threshold tuning by directly assessing semantic changes. However, the SMT concept is method-agnostic and can work with any similarity detection approach that suits your needs.
