# RAG Customer Support Assistant — Algérie Télécom

An intelligent virtual assistant built on a **Retrieval-Augmented Generation (RAG)** architecture combined with an **intent/smalltalk classification** module, designed to automate and personalize customer support for Algérie Télécom. The system runs **fully locally** (local embedding model, local vector store, local LLM).

Developed as part of a Master's thesis (M2) in Artificial Intelligence.

---

## Overview

The Chatbot assistant is built around a **RAG (Retrieval-Augmented Generation)** pipeline, using a **local pretrained LLM** that acts both as the **NLP/NLU engine** (understanding and classifying the user's message) and as the **generation engine** (producing the final answer from the retrieved context).

The system retrieves relevant chunks from a local knowledge base and generates a grounded, context-aware response using the local LLM.

## Architecture

### 1. Knowledge preparation (offline)

```
KB JSON files (kb_articles, kb_faq, kb_services, kb_rules)
        │
        ▼
   ingest.py (read + transform)
        │
        ▼
      Chunks
        │
        ▼
Embedding model (local): all-MiniLM-L6-v2
        │
        ▼
     Embeddings
        │
        ▼
Local vector store: FAISS index + chunks.json
        (stored in data/vector_store)
```

### 2. RAG search (online)

```
User question
     │
     ▼
Streamlit UI (ui.py)
     │
     ▼
main.py ──► Smalltalk (greeting / thanks)
     │
     ▼ (if real question)
Question encoding (all-MiniLM-L6-v2, local)
     │
     ▼
Retriever (retriever.py) ◄── store.py: load_index()
     │
     ▼
Top-k relevant chunks
     │
     ▼
build_context()
     │
     ▼
Augmented prompt
```

### 3. Response generation

```
Augmented prompt ──► Local LLM: Ollama + Phi-3 ──► Final response ──► User
```

### Sequence diagram

```
User ──"asks a question"──► UI
UI ──"forwards the question"──► Main module
Main module ──"searches for relevant context"──► RAG module
RAG module ──"returns context"──► Main module
Main module ──"sends prompt"──► Local language model
Local language model ──"returns generated response"──► Main module
Main module ──"forwards response"──► UI
UI ──"displays response"──► User
```

## Project Structure

```
app/
├── main.py                  # Application entry point, smalltalk routing
├── ui.py / ui2.py           # Streamlit user interface
├── intent_classifier.py     # Intent / smalltalk classification
├── generate_dataset.py      # Training data generation/preparation
├── rag/
│   ├── ingest.py            # KB reading, transformation, chunking
│   ├── retriever.py         # Semantic search over the vector store
│   ├── store.py             # FAISS index loading (load_index)
│   └── build_context()      # Builds the augmented prompt from top-k chunks
├── models/all-MiniLM-L6-v2  # Local embedding model
└── assets/                  # Static resources

data/
├── kb/                      # Source knowledge base (JSON files)
├── nlu/                     # Training data for intent classification
├── raw/                     # Raw data
└── vector_store/            # FAISS index + chunks.json
```

## Tech Stack

- **Language**: Python
- **UI**: Streamlit
- **Embeddings**: sentence-transformers (`all-MiniLM-L6-v2`, local)
- **Vector search**: FAISS (local)
- **LLM**: Ollama + Phi-3 (local, no external API calls)
- **NLU**: intent/smalltalk classification

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

## Future Improvements
- **Client API integration** — add an API to fetch client information on request (e.g. subscription details, invoices, ticket status) and link it to the client's database, enabling truly personalized responses.
- **Conversation memory** — keep track of previous exchanges to support multi-turn, context-aware conversations instead of treating each question independently.
- **Hybrid retrieval** — combine vector search with keyword-based search (e.g. BM25) to improve retrieval accuracy on exact terms (offer names, error codes).
- **Personalization via customer profile** — connect to Algérie Télécom's CRM/subscriber data to tailor answers to the user's actual plan, contract, or ticket history.
- **Evaluation pipeline** — add automated metrics (retrieval precision, answer relevance, latency) to measure and track performance over time.
- **Larger or hosted LLM option** — allow switching between the local Phi-3 model and a more powerful hosted model for higher-quality answers when needed.
- **Multilingual support** — extend intent classification and generation to Algerian Arabic (Darja) and Tamazight, in addition to French.
- **Deployment** — package the app with Docker and expose it via an API for integration into Algérie Télécom's existing customer channels (website, mobile app).
- **Logging & feedback loop** — collect user feedback on answers to progressively improve the knowledge base and retrieval quality.


## Screenshot
<img width="1821" height="882" alt="demo" src="https://github.com/user-attachments/assets/74a2cb6a-3819-4b69-a980-979136ac8d1b" />

## Author

**Abderrahmen Tamamra** 



