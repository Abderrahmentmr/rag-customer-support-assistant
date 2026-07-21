# RAG Customer Support Assistant — Algérie Télécom

An intelligent virtual assistant built on a **Retrieval-Augmented Generation (RAG)** architecture combined with an **intent classification** module, designed to automate and personalize customer support for Algérie Télécom.

Developed as part of a Master's thesis (M2) in Artificial Intelligence.

---

## Overview

The system combines two complementary approaches:

1. **Intent Classification (NLU)** — quickly identifies the user's need (billing, technical issue, offers, etc.) using a trained classifier on annotated data.
2. **RAG (Retrieval-Augmented Generation)** — for open-ended queries, retrieves relevant documents from a vectorized knowledge base, then generates a grounded, context-aware response.

This hybrid design reduces hallucinations and improves response relevance compared to a traditional rule-based or keyword-matching chatbot.

## Architecture

```
User query
    │
    ▼
Intent Classifier ──► Detected intent ──► Targeted response
    │
    ▼ (if intent is open-ended / out of scope)
Embedding (all-MiniLM-L6-v2)
    │
    ▼
Vector search (vector_store)
    │
    ▼
Response generation (LLM + retrieved context)
```

## Project Structure

```
app/
├── main.py                  # Application entry point
├── ui.py / ui2.py           # User interface (versions)
├── intent_classifier.py     # User intent classification
├── generate_dataset.py      # Training data generation/preparation
├── rag/                     # Retrieval-augmented generation pipeline
├── models/all-MiniLM-L6-v2  # Local embedding model (sentence-transformers)
└── assets/                  # Static resources

data/
├── kb/                      # Knowledge base (source documents)
├── nlu/                     # Training data for intent classification
├── raw/                     # Raw data
└── vector_store/            # Vector index for semantic search
```

## Tech Stack

- **Language**: Python
- **Embeddings**: sentence-transformers (`all-MiniLM-L6-v2`)
- **Vector search**: local vector store (FAISS/Chroma)
- **NLU**: supervised intent classification
- **Interface**: Python application (`ui.py`)

## Installation

```bash
git clone https://github.com/Abderrahmentmr/rag-customer-support-assistant.git
cd rag-customer-support-assistant
pip install -r requirements.txt
```

## Usage

```bash
python app/main.py
```

## Author

**Abderrahmen Tmr** — M2 Artificial Intelligence

## License

This project is distributed under the MIT License.
