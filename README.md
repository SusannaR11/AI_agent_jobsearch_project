# AI agent / RAG project using Arbetsförmedlingen data   
### An intelligent search and analysis application using RAG (Retrieval-Augmented Generation) to help users navigate Swedish labor market forecasts from Arbetsförmedlingen.
### Developed as part of the course Advanced Object-Oriented Programming 2 at NBI/Handelsakademin.
Authors:      
Susanna Rokka 
Susanne Wenblad

# -----------------------------------------------------

## Tech Stack
- Backend: FastAPI
- Vektordatabas: LanceDB
- Frontend: Streamlit
- AI-Modeller: * LLM: Google Gemini 2.5 Flash (via Pydantic AI)
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Datahantering: Pandas och DuckDB för ranking och filtrering


## Project-struktur
src/ai_agent_jobsearch_project/
├── assets/             # Bilder och logotyper
├── backend/            # FastAPI (rokka_api.py & wenblad_api.py), Scheman och Settings
├── frontend/           # Streamlit (main_app.py) och API-klient
├── services/           # LLM-agent, RAG-logik och Ingestion
└── data/               # Lokala databaser och JSON-filer

## Installation

1. ### Clone the repository:
git clone https://github.com/SusannaR11/AI_agent_jobsearch_project.git
cd AI_agent_jobsearch_project

2. ### Set up a virtual environment and install dependencies:
   - python -m venv .venv
   - source .venv/Scripts/activate # For Windows/Git Bash
   - source .venv/bin/activate  # For Mac
   - pip install -r requirements.txt
   - pip install -e .

3. ### Configure Environment Variables: 
Create a .env file in the root directory and add your API key:   
   - GOOGLE_API_KEY=your_secret_gemini_api_key


## Running the Application
The application utilizes a dual-backend architecture to separate labor market forecasts from real-time job advertisements.
The API:s run on different ports. 


### Usage Chatbot - prognosis        
1. Data Ingestion - Occupational Forecast API  (First time only)   
      Populate the vector database:
      python -m src.ai_agent_jobsearch_project.scrpits/dev__main.py
         

1. Start the Backends (Run in two separate terminals)
        Market Insights API (Port 8000):
        uvicorn src.ai_agent_jobsearch_project.backend.rokka_api:app --port 8000 --reload

        Occupational Forecast API (Port 8001):
        uvicorn src.ai_agent_jobsearch_project.backend.wenblad_api:app --port 8001 --reload

2. Start the Frontend (Run in a third terminal)       
        streamlit run src/ai_agent_jobsearch_project/frontend/main_app.py


