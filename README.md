# AI agent / RAG project using Arbetsförmedlingen data   
### An intelligent search and analysis application using RAG (Retrieval-Augmented Generation) to help users navigate Swedish labor market forecasts from Arbetsförmedlingen.
### Developed as part of the course Advanced Object-Oriented Programming 2 at NBI/Handelsakademin.
Authors:      
Susanna Rokka 
Susanne Wenblad

# -----------------------------------------------------

## Tech Stack
- Backend: FastAPI (Python <3)
- Vektordatabas: LanceDB
- Frontend: Streamlit
- AI-Modeller: * LLM: Google Gemini 2.5 Flash (via Pydantic AI)
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Datahantering: Pandas för ranking och filtrering


## Project-struktur
src/ai_agent_jobsearch_project/
├── backend/            # FastAPI, Scheman och Settings
├── services/           # Ranking, LLM-agent och Ingestion
├── embeddings/         # Vektorhantering och Document Builder
└── frontend/           # Streamlit-app och API-klient


## Installation

1. ### Clone the repository:
   git clone [(https://github.com/SusannaR11/AI_agent_jobsearch_project.git)]

2. ### Set up a virtual environment and install dependencies:
   - python -m venv .venv
   - source .venv/Scripts/activate # For Windows/Git Bash
   - source .venv/bin/activate  # For Mac
   - pip install -r requirements.txt
   - pip install -e .

3. ### Configure Environment Variables: 
Create a .env file in the root directory and add your API key:   
   - GOOGLE_API_KEY=your_secret_gemini_api_key


## Run applikation
The application has dual API:s - one deditacted to the prognosis chatbot and one dedicated to the current occuapation.   
The API:s run on different ports. 


### Usage Chatbot - prognosis        --> ÄNDRA EFTER ATT INGESTION ÄR KLAR!!!!!
1. Data Ingestion (First time only)   
      Populate the vector database:
      python -m src.ai_agent_jobsearch_project.services.ingestion_services
         

2. Run the API (Backend)
      Uses port 8001
      Open a terminal and start the FastAPI server:   
      fastapi dev src/ai_agent_jobsearch_project/backend/api.py

3. Run the UI (Frontend)
      Open a second terminal and start the Streamlit app:   
      streamlit run src/ai_agent_jobsearch_project/frontend/streamlit_app.py --> Ändra?


### Usage Chatbot - current occupations
1. Data Ingestion  
      
         

2. Run the API (Backend)
      Uses port 8000
      Open a terminal and start the FastAPI server:   
      fastapi dev src/ai_agent_jobsearch_project/backend/api.py --> Ändra till rätt namn

3. Run the UI (Frontend)
      Open a second terminal and start the Streamlit app:   
      streamlit run src/ai_agent_jobsearch_project/frontend/streamlit_app. --> Ändra?