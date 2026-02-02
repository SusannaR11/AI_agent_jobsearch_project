import streamlit as st
import requests
from ai_agent_jobsearch_project.frontend.api_client import get_areas, get_forecast
 

if "areas" not in st.session_state:
    st.session_state.areas = None

if "selected_area" not in st.session_state:
    st.session_state.selected_area = None


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




#============= HUVUDSIDA ================
st.divider()

st.subheader("Sök prognos")
st.text("Här söker du prognos för ett valt yrke. Du får information om framtida jobbmöjligheter.")
st.text("Resultatet visar nationella prognos. Du kan även välja att se prognos för ett specifikt yrke inom ett län.")


query_yrke = st.text_input("Skriv ett yrke", placeholder="t.ex. systemutvecklare inom IT")

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
            lan= None,
            limit=5
        )
    except Exception as e:
        st.error(f"Kunde inte hämta prognos: {e}")
        st.stop()
    
    if not results:
        st.info("Inga träffar. Testa ett annat yrke!")
        st.stop()
    
    st.success(f"Hittade {len(results)} träffar")
    for r in results:
        st.markdown(f"### {r['yb_yrke']} ({r['lan']})")
        st.write(f"**Prognos:** {r.get('prognos', '')}")
        st.write(f"**Jobbmöjligheter:** {r.get('jobbmojligheter', '')}")
        st.write(f"**Rekrytering:** {r.get('rekryteringssituation', '')}")

        with st.expander("Visa mer"):
            st.write(r.get("text_jobbmojligheter", ""))
            st.write(r.get("text_rekryteringssituation", ""))

        st.caption(f"distance: {r.get('distance', 0):.4f}")
