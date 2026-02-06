FROM python:3.11-slim

WORKDIR /main_app/frontend

# later in Docker compose we will use a context that is a parent of frontend folder. then we can send frontend folder by writing frontend
COPY src/ai_agent_jobsearch_project/frontend .

RUN pip install --no-cache-dir uv

RUN uv sync --no-dev

# run Streamlit frontend
# use variable PORT if it exists, otherwise it uses 8501. i n azure web app, PORT will be 80
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# for frontend azure port "--server.port=${PORT:-8501}", "--server.port=8501"