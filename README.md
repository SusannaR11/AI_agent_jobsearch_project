# AI Agent / RAG Project Using Arbetsförmedlingen Data

An intelligent search and analysis application using Retrieval-Augmented Generation (RAG) to help users navigate Swedish labor market forecasts from Arbetsförmedlingen.

Developed as part of the course  
Advanced Object-Oriented Programming 2  
at NBI / Handelsakademin

## Authors
- Susanna Rokka  
- Susanne Wenblad  

---

## Tech Stack

- Backend: FastAPI  
- Vector Database: LanceDB  
- Frontend: Streamlit  
- AI Models:
  - LLM: Google Gemini 2.5 Flash (via Pydantic AI)
- Embeddings: sentence-transformers/all-MiniLM-L6-v2  
- Data Handling: Pandas and DuckDB for ranking and filtering  

---

## Project Structure
src/ai_agent_jobsearch_project/
├── assets/ # Images and logos
├── backend/ # FastAPI backends (rokka_api.py, wenblad_api.py)
├── frontend/ # Streamlit app (main_app.py) and API client
├── services/ # LLM agent, RAG logic and ingestion
└── data/ # Local databases and JSON files



## Installation

1. ### Clone the repository:
git clone https://github.com/SusannaR11/AI_agent_jobsearch_project.git
cd AI_agent_jobsearch_project

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