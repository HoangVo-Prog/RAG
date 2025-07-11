# RAG

# 📘 PDF RAG Assistant – Project

A Vietnamese-language PDF question-answering application, built using the **RAG (Retrieval-Augmented Generation)** architecture. It combines a **LLM (Vicuna 7B)** with **semantic chunking** techniques. The interface is built with **Streamlit**, allowing users to upload documents, ask questions, and receive automatic answers.

---

## 🧱 Directory Structure & Description

```plaintext
rag/
│
├── main.py                  # Entry point of the Streamlit app
├── requirements.txt         # Required Python packages
├── config.py                # (Optional) Global configuration
├── api.py                   # (Optional) REST API starter
├── .env                     # (Optional) Environment variables like API keys
│
├── app/
│   ├── core/                # Core logic: load model, process PDF, build RAG chain
│   │   ├── embeddings.py    # Load embedding model
│   │   ├── llm.py           # Load Vicuna LLM
│   │   ├── pdf.py           # PDF handling: chunking, vector DB, build chain
│   │   └── prompt.py        # (Optional) Custom prompt templates
│   │
│   ├── ui/                  # Streamlit user interface
│   │   ├── interface.py     # Main UI: upload, ask, answer
│   │   └── __init__.py
│   │
│   ├── services/            # (Optional) Middleware logic
│   │   └── question_handler.py  # (Currently empty) manages Q&A, history, formatting
│   │
│   └── api/                 # (Optional) REST API with FastAPI
│       ├── __init__.py
│       ├── routes.py        # Defines endpoints like /ask
│       └── schemas.py       # Pydantic data models
│
└── utils/                   # Shared utilities
    ├── logger.py            # (Optional) Logging to console/file
    └── file.py              # (Optional) File upload, validation, etc.
```

---

## 🔁 Basic Pipeline

![Alt text](./images/baseline_pipeline.png)

---

## 🚀 How to Run

```bash
# Create environment and install dependencies
bash setup.sh

# Or manually:
conda create -n aio-rag python=3.11
conda activate aio-rag
pip install -r requirements.txt

# Launch the app
streamlit run main.py
