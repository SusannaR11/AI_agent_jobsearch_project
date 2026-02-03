import streamlit as st
import requests
from difflib import get_close_matches   #Tips från ChatGPT - används för att matcha användarens imatade yrke mot yrken i yrkesbarometern
from ai_agent_jobsearch_project.frontend.constants import LAN_OPTIONS
from ai_agent_jobsearch_project.frontend.api_client import (
    get_areas,
    get_forecast,
    get_occupations,
)


#===================== Hjälpfunktion - länskoder  =====================
LAN_CODE_TO_NAME = dict(LAN_OPTIONS)  # "" -> "Nationellt ...", "03" -> "Uppsala län", osv


#===================== Session state =====================
if "areas" not in st.session_state:
    st.session_state.areas = None

if "selected_area" not in st.session_state:
    st.session_state.selected_area = None

if "limit" not in st.session_state:
    st.session_state.limit = 5

if "lan" not in st.session_state:
    st.session_state.lan = None

if "occupations" not in st.session_state:
    st.session_state.occupations = None

if "messages" not in st.session_state:
    st.session_state.messages = []


#===================== Konfiguration =====================
st.set_page_config(page_title="Yrkesbarometern")
st.title("Yrkesbarometern")
st.subheader("Hur ser framtiden ut för det valda yrke?")

API_BASE = "http://127.0.0.1:8000"
SHOW_MANUAL_UI = False


#===================== SIDOMENY =====================
with st.sidebar:
    with st.expander("Teknisk information"):
        st.caption("GET /health")
        st.write("Appen kör ✔️")

        if st.button("Testa backend"):
            try:
                response = requests.get(f"{API_BASE}/health", timeout=5)
                st.json(response.json())
            except Exception as e:
                st.error(f"Kunde inte nå backend: {e}")

    st.divider()
    st.subheader("Välj yrkesområde")

    if st.button("Ladda yrkesområden"):
        try:
            st.session_state.areas = get_areas()
        except Exception as e:
            st.error(f"Kunde inte hämta yrkesområden: {e}")

    if st.session_state.areas:
        st.session_state.selected_area = st.selectbox(
            "Yrkesområde",
            st.session_state.areas,
        )

    st.divider()
    st.subheader("Yrken (för chat-matchning)")

    if st.button("Ladda yrken"):
        if not st.session_state.selected_area:
            st.warning("Välj yrkesområde först.")
        else:
            try:
                st.session_state.occupations = get_occupations(
                    yrkesomrade=st.session_state.selected_area,
                    lan=st.session_state.lan,
                )
                st.success(f"Hämtade {len(st.session_state.occupations)} yrken.")
            except Exception as e:
                st.error(f"Kunde inte hämta yrken: {e}")

    st.divider()
    st.subheader("Filtera din sökning")

    st.session_state.limit = st.slider(
        "Antal träffar",
        min_value=1,
        max_value=15,
        value=st.session_state.limit,
    )

    st.divider()
    st.subheader("Län (valfritt)")

    lan_labels = [f"{code} - {name}" if code else name for code, name in LAN_OPTIONS] #OBS! Detta är inte egen kod, utan kod genererad från ChatGPT pga ville få till en lösning med namn på län ist för länskoder
    lan_codes = [code for code, _ in LAN_OPTIONS]

    current_code = st.session_state.lan or ""
    current_index = lan_codes.index(current_code) if current_code in lan_codes else 0

    chosen = st.selectbox("Välj län", lan_labels, index=current_index)

    chosen_index = lan_labels.index(chosen)
    chosen_code = lan_codes[chosen_index]
    st.session_state.lan = chosen_code if chosen_code else None


#===================== HUVUDSIDA: chat-historik =====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


#===================== UI för felsökning - ej aktiverat per default =====================
if SHOW_MANUAL_UI:
    st.divider()
    st.info(" UI för felsökning är på ")

    if st.session_state.occupations:
        selected = st.selectbox("Välj yrke", st.session_state.occupations)
        if st.button("Visa prognos"):
            results = get_forecast(
                yrkesomrade=st.session_state.selected_area,
                query_yrke=selected,
                lan=st.session_state.lan,
                limit=st.session_state.limit,
            )
            st.write(results)


#===================== CHAT INPUT =====================
st.divider()
user_input = st.chat_input("Fråga mig om ett yrke, t.ex. 'Hur ser framtiden ut för mjukvaruutvecklare?'")


def match_occupation(user_text: str, occupations: list[str]) -> str | None:
    """
    Matches users text to a list of occupations from Yrkesbarometern.           
    1) exact match (case-insensitive)
    2) fuzzy match with difflib
    """
    q = user_text.strip()
    if not q:
        return None

    #Exakt match mot det yrke som anväbdaren registrerat
    for y in occupations:
        if y.lower() == q.lower():
            return y

    #Fuzzy match
    matches = get_close_matches(q, occupations, n=1, cutoff=0.6)
    if matches:
        return matches[0]

    return None


if user_input:
    
    st.session_state.messages.append({"role": "user", "content": user_input})

   
    if not st.session_state.selected_area:
        assistant_text = "Välj först ett **yrkesområde** i sidomenyn."
    elif not st.session_state.occupations:
        assistant_text = "Klicka **Ladda yrken** i sidomenyn så jag vet vilka yrken jag kan matcha mot."
    else:
        matched_yrke = match_occupation(user_input, st.session_state.occupations)

        if not matched_yrke:            
            examples = ", ".join(st.session_state.occupations[:5])
            assistant_text = (
                "Jag kunde inte matcha yrket du skrev mot kända yrken inom valt område.\n\n"
                f"Exempel på yrken i detta område: **{examples}**\n\n"
                "Testa att skriva ett av dem (eller välj annat yrkesområde)."
            )
        else:
            
            results = get_forecast(
                yrkesomrade=st.session_state.selected_area,
                query_yrke=matched_yrke,
                lan=st.session_state.lan,
                limit=st.session_state.limit,
            )

            if not results:
                assistant_text = (
                    f"Jag tolkar ditt yrke som **{matched_yrke}**, men hittade ingen prognos just nu. "
                    "Testa ett annat yrke eller byt yrkesområde."
                )
            else:
                top = results[0]
                alternatives = "\n".join(
                    [
                        f"- {r.get('yb_yrke','')} ({LAN_CODE_TO_NAME.get(r.get('lan',''), 'Nationellt')})"
                        for r in results[1:4]
                    ]
                )

                assistant_text = f"""Jag tolkar ditt yrke som **{matched_yrke}**.

- Prognos: {top.get('prognos','')}
- Jobbmöjligheter: {top.get('jobbmojligheter','')}
- Rekrytering: {top.get('rekryteringssituation','')}

**Alternativ jag också hittade:**
{alternatives if alternatives else "- (inga fler förslag)"}
"""

    st.session_state.messages.append({"role": "assistant", "content": assistant_text})

    st.rerun()
