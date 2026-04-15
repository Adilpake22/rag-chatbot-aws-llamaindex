# RAG Chatbot — AWS + LlamaIndex + Groq

An end-to-end RAG chatbot that answers questions 
from documents stored in AWS S3.

## Live Demo
Coming soon — AWS App Runner deployment

## Architecture
- Documents stored in AWS S3
- HuggingFace BGE embeddings (local, free)
- LlamaIndex RAG pipeline
- Groq LLaMA3 for answer generation
- Streamlit chat UI

## Tech Stack
| Layer | Technology |
|---|---|
| Storage | AWS S3 |
| Embeddings | HuggingFace BGE |
| RAG Framework | LlamaIndex |
| LLM | Groq LLaMA3 |
| UI | Streamlit |
| Language | Python 3.11 |

## Setup

1. Clone the repo
git clone https://github.com/Adilpake22/rag-chatbot-aws-llamaindex

2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Copy env file and fill values
cp .env.example .env

5. Run the app
streamlit run app.py

## Project Structure
rag-chatbot-aws-llamaindex/
├── app.py              # Streamlit UI
├── agent.py            # RAG pipeline
├── requirements.txt    # Dependencies
├── Dockerfile          # Container setup
├── .env.example        # Environment template
└── README.md           # This file

## Features
- Upload documents locally or load from S3
- Ask questions in natural language
- Get grounded answers from documents
- Fast responses using Groq LLaMA3

## Screenshots

<img width="1913" height="966" alt="image" src="https://github.com/user-attachments/assets/848c5afc-630f-4907-838b-3837d85438f7" />
<img width="1915" height="963" alt="image" src="https://github.com/user-attachments/assets/427616a9-771c-4ac6-b8a0-f96ba1c02c3f" />

