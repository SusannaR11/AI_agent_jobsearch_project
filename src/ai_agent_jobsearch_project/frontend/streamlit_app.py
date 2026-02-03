import streamlit as st
import requests
from ai_agent_jobsearch_project.frontend.api_client import get_areas, get_forecast, get_occupations
from ai_agent_jobsearch_project.frontend.constants import LAN_OPTIONS


LAN_CODE_TO_NAME = dict(LAN_OPTIONS)    # Omvandlar länskod + län till en dict; "" -> "Nationellt ...", "03" -> "Uppsala län", osv



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


#=========== Konfiguration av sidan ==============
st.set_page_config(page_title="Yrkesbarometern")
st.title("Yrkesbarometern")
st.subheader("Hur ser framtiden ut för det valda yrke?")


API_BASE = "http://127.0.0.1:8000"


#============= SIDOMENY ================
#----------- Kontroll av api -----------
with st.sidebar:    
    with st.expander("Teknisk information"):
        st.caption("GET /health")
        st.write("Appen kör ✔️")
        
        if st.button("Testa backend"):
            try:
                response = requests.get(f"{API_BASE}/health", timeout=5)
                st.json(response.json())

            except Exception as e:
                st.error(f"Kunde inte nå backend {e}")


    #----------- Hämta yrkesområde -----------
    st.divider()
    st.subheader("Välj yrkesområde")

    if st.button("Ladda yrkesområden"):
        try:
            st.session_state.areas = get_areas()

        except Exception as e:
            st.error(f"Kunde inte hämta yrkesområden: {e}")
        
    if st.session_state.areas:
        st.session_state.selected_area = st.selectbox("Yrkesområde", st.session_state.areas)
    
    st.divider()
    st.subheader("Yrke")

    if st.button("Ladda yrken"):
        try:
            st.session_state.occupations = get_occupations(
                yrkesomrade=st.session_state.selected_area,
                lan=st.session_state.lan
            )
        except Exception as e:
            st.error(f"Kunde inte hämta yrken: {e}")

    
    st.divider()
    st.subheader(f"**Filtera din sökning**")

    st.session_state.limit = st.slider(
        "Antal träffar",
        min_value=1,
        max_value=15,
        value=st.session_state.limit
    )
    st.divider()
    st.subheader("Län (valfritt)")

    lan_labels = [                              ###OBS! Detta är inte egen kod, utan kod genererad från ChatGPT pga ville få till en lösning med namn på län ist för länskoder
        f"{code} - {name}" if code else name
        for code, name in LAN_OPTIONS
    ]
    lan_codes = [code for code, _ in LAN_OPTIONS]

    current_code = st.session_state.lan or ""
    current_index = lan_codes.index(current_code) if current_code in lan_codes else 0

    chosen = st.selectbox("Välj län", lan_labels, index=current_index)

    # Hitta tillbaka till kod via index
    chosen_index = lan_labels.index(chosen)
    chosen_code = lan_codes[chosen_index]

    st.session_state.lan = chosen_code if chosen_code else None





#============= HUVUDSIDA ================
st.divider()

st.subheader("Sök prognos")
st.text("Här söker du prognos för ett valt yrke. Du får information om framtida jobbmöjligheter.")
st.text("Resultatet visar nationella prognos. Du kan även välja att se prognos för ett specifikt yrke inom ett län.")


if st.session_state.occupations:
    query_yrke = st.selectbox("Välj yrke", st.session_state.occupations)
else:
    st.info("Ladda yrken i sidomenyn för att välja yrke.")
    query_yrke = ""

if st.button("Visa prognos"):
    if not st.session_state.selected_area:
        st.warning("Välj ett yrkesområde i sidomenyn först")
        st.stop()

    if not query_yrke.strip():
        st.warning("Skriv ett yrke först")
        st.stop()

    try:
        results = get_forecast(
            yrkesomrade=st.session_state.selected_area,
            query_yrke=query_yrke,
            lan= st.session_state.lan,
            limit=st.session_state.limit
        )
    except Exception as e:
        st.error(f"Kunde inte hämta prognos: {e}")
        st.stop()
    
    if not results:
        st.info("Inga träffar. Testa ett annat yrke!")
        st.stop()
    
    st.success(f"Hittade {len(results)} träffar")

    if st.session_state.lan:
        st.info(f"Visar prognos för län: {st.session_state.lan}")
    else:
        st.info("Visar nationell prognos för yrket.")

    for r in results:
        lan_code = r.get("lan", "")
        lan_name = LAN_CODE_TO_NAME.get(lan_code, "Nationellt (ingen filtrering på län)")

        st.markdown(f"### {r['yb_yrke']} - {lan_name}")
        st.write(f"**Prognos:** {r.get('prognos', '')}")
        st.write(f"**Jobbmöjligheter:** {r.get('jobbmojligheter', '')}")
        st.write(f"**Rekrytering:** {r.get('rekryteringssituation', '')}")

        with st.expander("Visa mer"):
            st.write(r.get("text_jobbmojligheter", ""))
            st.write(r.get("text_rekryteringssituation", ""))

        st.caption(f"distance: {r.get('distance', 0):.4f}")
