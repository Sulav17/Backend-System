# 🧠 FastAPI RAG Backend System (Containerized)

This is a fully containerized Retrieval-Augmented Generation (RAG) backend system built with FastAPI, LangChain, Celery, and Qdrant. It allows intelligent file processing, conversational memory, agentic reasoning, and interview scheduling — all without any UI.

---

## 🚀 Features

- 📤 **File Upload & Indexing**
  - Accepts `.pdf` or `.txt` files.
  - Supports recursive or semantic chunking.
  - Embeds chunks using models (OpenAI, HuggingFace, or custom).
  - Stores embeddings in **Qdrant**.
  - Logs metadata (chunking method, model used, etc.) in MongoDB.

- 🤖 **Agentic RAG API**
  - Implements a **LangChain Agent** (not RetrievalQA).
  - Dynamically reasons with tools to retrieve and respond.
  - Uses **Redis** for persistent conversational memory.

- 📅 **Interview Booking API**
  - Collects name, email, and preferred date/time.
  - Sends confirmation email via **SMTP** using **Celery**.
  - Booking data is stored in MongoDB.

- 📊 **Comparison Tools**
  - Evaluate and compare:
    - Chunking strategies (recursive vs semantic).
    - Similarity search algorithms supported by Qdrant.
  - Generates a findings report (latency + retrieval accuracy).

---

## 🛠️ Technologies Used

| Component | Tech |
|----------|------|
| Web Framework | FastAPI |
| Embeddings | LangChain, HuggingFace, OpenAI |
| Vector DB | Qdrant (📦 containerized) |
| Memory Store | Redis |
| Task Queue | Celery |
| Message Broker | Redis |
| Email | SMTP |
| Storage | MongoDB |
| Containerization | Docker, Docker Compose |

---


## 🧪 How to Run Locally (Dockerized)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/fastapi-rag-backend.git
cd fastapi-rag-backend
cp .env.example .env
docker compose up -d
