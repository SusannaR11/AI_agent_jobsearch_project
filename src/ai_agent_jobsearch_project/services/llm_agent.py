import os
from pydantic_ai import Agent
from ai_agent_jobsearch_project.backend.schemas import LLMAnalysis, OccupationMatch
from ai_agent_jobsearch_project.backend.settings import get_gemini_api_key

api_key = get_gemini_api_key()

agent = Agent(
    "google-gla:gemini-2.5-flash",
    system_prompt=(
    "Du är en expert på den svenska arbetsmarknaden. "
    "Svara pedagogiskt baserat på bifogad fakta. "
    "Ditt svar SKA bestå av två delar: "
    "1. En sammanfattning av prognosen. "
    "2. Ett konkret tips/rekommendation. "    
    )
)

def generate_chat_analysis(user_query: str, matches: list[OccupationMatch]) -> LLMAnalysis:
    if not matches:
        return LLMAnalysis(
            summary="Jag hittade tyvärr ingen data för det yrket just nu.",
            recommendation="Försök söka på ett annat yrke eller område."
        )

    context_str = "\n".join([
        f"Yrke: {m.yb_yrke}, Prognos: {m.prognos}, Beskrivning: {m.text_jobbmojligheter}" 
        for m in matches
    ])
    
    result = agent.run_sync(f"Användarens fråga: {user_query}\n\nFakta:\n{context_str}")
    
    return LLMAnalysis(
        summary=result.output, 
        recommendation="Läs mer om yrket i underlaget nedan."
    )