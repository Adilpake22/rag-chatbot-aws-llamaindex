# RAG Chatbot — AWS S3 + LlamaIndex + Groq

An end-to-end Retrieval-Augmented Generation (RAG) chatbot that answers questions from documents stored in AWS S3 or uploaded locally. Built with LlamaIndex, Groq LLaMA3, and HuggingFace embeddings — deployed on Streamlit Cloud.

---

## Live Demo

🔗 [Launch App on Streamlit Cloud](https://your-app-name.streamlit.app) 

---

## Architecture
<img width="1585" height="863" alt="image" src="https://github.com/user-attachments/assets/2e1c3673-40a1-4322-953a-21bfc6159c4f" />

---

> **Services used:**
> - **AWS S3** — stores PDF and TXT documents
> - **AWS IAM** — credentials for programmatic S3 access via boto3
> - *(OpenSearch & App Runner planned — blocked by billing)*

---

## Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Document Storage | AWS S3 | Free tier (5 GB) |
| Embeddings | HuggingFace BGE (`bge-small-en-v1.5`) | Local, free, no API key |
| RAG Framework | LlamaIndex | VectorStoreIndex (in-memory) |
| LLM | Groq — LLaMA 3.3 70B | Free tier API |
| UI | Streamlit | Deployed on Streamlit Community Cloud |
| Language | Python 3.11 | |
| PDF Parsing | pypdf | |

---

## Features

- Upload documents locally (PDF or TXT) or load directly from your S3 bucket
- Ask questions in natural language and get grounded answers from the document
- Fast response times powered by Groq's LLaMA 3.3 70B
- Free-tier friendly — no paid services required to run the full demo
- Clean chat UI with message history and a clear chat button

---

## Project Structure

```
rag-chatbot-aws-llamaindex/
├── app.py              # Streamlit UI — chat interface, sidebar, session state
├── agent.py            # RAG pipeline — ingest, embed, query
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container setup (optional local run)
├── .env.example        # Environment variable template
└── README.md           # This file
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Adilpake22/rag-chatbot-aws-llamaindex
cd rag-chatbot-aws-llamaindex
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```dotenv
AWS_ACCESS_KEY_ID=your-access-key-here
AWS_SECRET_ACCESS_KEY=your-secret-key-here
AWS_DEFAULT_REGION=ap-south-1
S3_BUCKET_NAME=your-bucket-name-here
GROQ_API_KEY=your-groq-key-here
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## Streamlit Cloud Deployment

If deploying on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push your code to a public GitHub repo
2. Go to Streamlit Cloud → **New app** → connect your repo
3. In **Settings → Secrets**, add your credentials in TOML format:

```toml
AWS_ACCESS_KEY_ID = "your-access-key-here"
AWS_SECRET_ACCESS_KEY = "your-secret-key-here"
AWS_DEFAULT_REGION = "ap-south-1"
S3_BUCKET_NAME = "your-bucket-name-here"
GROQ_API_KEY = "your-groq-key-here"
```

> **Note:** The `.env` file is not used on Streamlit Cloud. All secrets go through the Streamlit Secrets manager. Update `agent.py` to use `st.secrets["KEY"]` instead of `os.getenv("KEY")` when deploying.

---

## How It Works

1. **Document ingestion** — You upload a PDF/TXT locally or select a file from your S3 bucket. The file is parsed by `pypdf` or plain text read and passed to LlamaIndex.
2. **Embedding** — LlamaIndex chunks the document and runs each chunk through the HuggingFace BGE model locally to create embeddings.
3. **Index** — Embeddings are stored in an in-memory `VectorStoreIndex` tied to the current session.
4. **Query** — When you ask a question, the top 3 most relevant chunks are retrieved via similarity search and passed to Groq's LLaMA 3.3 70B along with your question.
5. **Answer** — The LLM generates a grounded answer and it appears in the chat.

---

## Screenshots

### Load from S3 + Chat
![S3 Load Screenshot](https://github.com/user-attachments/assets/848c5afc-630f-4907-838b-3837d85438f7)

### Local Upload + Answer
![Local Upload Screenshot](https://github.com/user-attachments/assets/427616a9-771c-4ac6-b8a0-f96ba1c02c3f)

## AWS Services

### S3 Bucket
<img width="1913" height="846" alt="s3 aws" src="https://github.com/user-attachments/assets/0d2a15f8-9556-40f8-be5d-9d88d8188e05" />

### AWS Knowledge Base
<img width="1888" height="842" alt="kb aws" src="https://github.com/user-attachments/assets/0f0326c0-6c49-4785-8a32-7cd667c0a72b" />


---

## Known Limitations

- Vector index is **in-memory only** — reloading the page clears it and the document must be re-ingested
- One document at a time — loading a new document replaces the previous index
- No conversation memory — each query is independent; prior chat turns are not sent to the LLM
- HuggingFace model downloads (~200 MB) on first cold start — Streamlit Cloud may be slow initially

---


## Author

**Adilpake22** — [@Adilpake22](https://github.com/Adilpake22)

---

