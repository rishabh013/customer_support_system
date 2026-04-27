# 🤖 Customer Support System — RAG Project

A Retrieval-Augmented Generation (RAG) based customer support chatbot built with LangChain, AstraDB, and FastAPI.

---

## 📁 Project Structure

```
customer_support_system/
│
├── data_ingestion/
│   └── ingestion_pipeline.py       # Loads, transforms & stores docs in vector DB
│
├── config/
│   └── config.yaml                 # Central config (models, DB, settings)
│
├── utils/
│   ├── config_loader.py            # Reads and parses config.yaml
│   └── model_loader.py             # Loads embedding & LLM models
│
├── retriever/
│   └── retrieval.py                # Vector DB retrieval logic
│
├── prompt_library/
│   └── prompt.py                   # Prompt templates for the LLM
│
├── static/
│   └── style.css                   # Frontend styles
│
├── templates/
│   └── chat.html                   # Chat UI template
│
├── main.py                         # FastAPI app entry point
├── setup.py                        # Package setup
├── requirements.txt                # Dependencies
└── .env                            # API keys (never commit this)
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd customer_support_system
```

### 2. Create a Virtual Environment
```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note:** `requirements.txt` includes `-e .` which automatically runs `setup.py` in editable mode.  
> After installation, verify with:
> ```bash
> pip show e-commerce-bot
> ```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
ASTRA_DB_API_ENDPOINT=your_astra_db_endpoint
ASTRA_DB_TOKEN=your_astra_db_token
ASTRA_DB_KEYSPACE='default_keyspace'
```

---

## 🚀 Running the Project

### Step 1: Ingest Data into Vector DB
```bash
python data_ingestion/ingestion_pipeline.py
```

### Step 2: Start the Application
```bash
uvicorn main:app --reload --port 8001
```

Then open your browser at: [http://localhost:8001](http://localhost:8001)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq / Google Gemini / OpenAI |
| Embeddings | Google Generative AI / OpenAI |
| Vector Store | DataStax AstraDB |
| Framework | LangChain |
| Backend | FastAPI |
| Frontend | HTML + CSS (Jinja2 templates) |

---

## 📌 Notes

- Make sure your AstraDB instance is **active** (free tier hibernates after inactivity — resume it from the [Astra dashboard](https://astra.datastax.com) before running ingestion).
- Model selection (LLM + embeddings) is controlled via `config/config.yaml` — no code changes needed to switch providers.


    
