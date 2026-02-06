FROM python:3.11-slim

WORKDIR /app

# copy uv files
COPY pyproject.toml uv.lock ./
COPY src/ai_agent_jobsearch_project ./src/ai_agent_jobsearch_project
COPY src/ai_agent_jobsearch_project/knowledge_base ../knowledge_base



# later in Docker compose we will use a context that is a parent of frontend folder. then we can send frontend folder by writing frontend
# WORKDIR /app/backend

# install uv
RUN pip install --no-cache-dir uv

WORKDIR /app/src/ai_agent_jobsearch_project/backend

RUN uv sync --no-dev --frozen

CMD ["uv", "run","uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "8001"]

# for azure deployment change port to "80"