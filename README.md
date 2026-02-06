# Labor Market Agent

### An intelligent search and analysis application using RAG (Retrieval-Augmented Generation) to navigate Swedish labor market forecasts and real-time job data.

Developed as part of the **Advanced Object-Oriented Programming 2** course at NBI/Handelsakademin.

**Authors:** Susanna Rokka & Susanne Wenblad

---

## Tech Stack
- **Backend:** FastAPI (Dual-instance architecture)
- **Vector Database:** LanceDB (for RAG) & DuckDB (for structured data)
- **Frontend:** Streamlit
- **AI Models:** - **LLM:** Google Gemini 2.0 Flash (implemented via Pydantic AI)
  - **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Data Processing:** Pandas & DuckDB for efficient ranking, filtering, and analysis.

## Project Structure
```text
src/ai_agent_jobsearch_project/
├── assets/             # Logos and visual assets
├── backend/            # FastAPI instances (rokka_api & wenblad_api), schemas, and settings
├── frontend/           # Streamlit main application and API clients
├── services/           # LLM Agent logic, RAG implementation, and data ingestion
└── data/               # Local databases (DuckDB/LanceDB) and raw JSON sources

--- 
```

## Installation


1. ### Clone the repository:
git clone https://github.com/SusannaR11/AI_agent_jobsearch_project.git
```
cd AI_agent_jobsearch_project
```

2. ### Set up a virtual environment and install dependencies:
python -m venv .venv
source .venv/Scripts/activate # For Windows/Git Bash
source .venv/bin/activate  # For Mac
pip install -r requirements.txt
pip install -e .

3. ### Configure Environment Variables: 
Create a .env file in the root directory and add your API key:   
GOOGLE_API_KEY=your_secret_gemini_api_key


## Running the Application
The application uses two backend APIs, each running on a separate port.

---

### Step 1: Data ingestion (first run only)
Populate the vector database with occupational forecasts:
python -m src.ai_agent_jobsearch_project.scripts/dev__main.py


### Step 2: Start the backends
Run each command in separate terminals.

Market Insights API (Port 8000):
uvicorn src.ai_agent_jobsearch_project.backend.rokka_api:app --port 8000 --reload

Occupational Forecast API (Port 8001):
uvicorn src.ai_agent_jobsearch_project.backend.wenblad_api:app --port 8001 --reload

### Step 3: Start the frontend
streamlit run src/ai_agent_jobsearch_project/frontend/main_app.py

---

## Usage

- Open the Streamlit interface in your browser
- Ask questions about occupations, demand forecasts, and labor market trends
- The system retrieves relevant documents using vector search and generates answers using the LLM

---