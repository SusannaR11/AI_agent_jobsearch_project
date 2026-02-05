import lancedb
from pydantic_ai import Agent
from ai_agent_jobsearch_project.frontend.constants import VECTOR_DATABASE_PATH
from ai_agent_jobsearch_project.backend.data_models import RagResponse

db = lancedb.connect(VECTOR_DATABASE_PATH)

rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        "You are a job market analyst.",
        "Answer only using retrieved job ad descriptions.",
        "Do not hallucinate.",
        "Keep answer short and clear, max 4 sentences.",
        "Answer only in Swedish."
    ),
    output_type=RagResponse,
)


@rag_agent.tool_plain
def retrieve_docs(query: str, k: int = 3) -> str:
    results = db["jobads"].search(query).limit(k).to_list()
    top = results[0]

    return f"""
    Occupation group: {top['occupation_group']}

    Job description:
    {top['content']}

    Base your answer only on this information.
    """
