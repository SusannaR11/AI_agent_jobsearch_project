import streamlit as st
import requests
from ai_agent_jobsearch_project.frontend.constants import LAN_OPTIONS
from ai_agent_jobsearch_project.frontend.api_client import get_areas, post_chat


#===================== Hjälpfunktioner =====================

#----------- Länskoder ------------
LAN_CODE_TO_NAME = dict(LAN_OPTIONS)  # "" -> "Nationellt ...", "03" -> "Uppsala län", osv

#----------- Cache ------------
@st.cache_data(show_spinner="AI:n tänker...")
def get_chat_response(yrkesomrade, message, lan):
    
    payload = {
        "yrkesomrade": yrkesomrade,
        "message": message,
        "lan": lan
    }
    response = requests.post(f"{API_BASE}/chat", json=payload)
    return response.json()

#===================== Session state =====================
if "areas" not in st.session_state:
    st.session_state.areas = None

if "selected_area" not in st.session_state:
    st.session_state.selected_area = None

if "lan" not in st.session_state:
    st.session_state.lan = None

if "occupations" not in st.session_state:
    st.session_state.occupations = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_usage" not in st.session_state:
    st.session_state.api_usage = 0


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

    with st.expander("API-Monitor"):                        #Kod genererad från Gemini för att ha koll på tokens. 
        # Beräkna status
        limit = 15  # Geminis vanliga RPM (Requests Per Minute) limit
        usage = st.session_state.api_usage
        
        # Visa en progress bar
        progress = min(usage / limit, 1.0)
        st.progress(progress)
        st.caption(f"Anrop: {usage} av {limit} (per minut)")
        
        if usage >= limit:
            st.error("⚠️ Gräns nådd! Vänta 60 sek.")
        elif usage > 10:
            st.warning("🟡 Närmar dig gränsen")
        else:
            st.success("🟢 API-status: OK")

        # Knapp för att nollställa räknaren manuellt om man vill
        if st.button("Nollställ mätare"):
            st.session_state.api_usage = 0

    st.divider()
    if st.button("Rensa konversation"):
        st.session_state.messages = []
        # Vi kan även nollställa vald sökning om vi vill
        st.session_state.selected_area = st.session_state.areas[0] if st.session_state.areas else None
        # För att tvinga Streamlit att rita om sidan direkt:
        st.rerun()


    st.header("Filtrera din sökning")
    st.subheader("Välj yrkesområde")

    if st.session_state.areas is None:
        try:           
            st.session_state.areas = get_areas()
        except Exception as e:
            st.error(f"Kunde inte ladda yrkesområden: {e}")            
            st.session_state.areas = ["Data/IT"]            #Tips från Gemini - Data/IT som default så nedanstående selctbox inte kraschar!

    selected_area = st.selectbox(
        "Välj yrkesområde", 
      options=st.session_state.areas
    )
    st.session_state.selected_area = selected_area

    lan_labels = [f"{code} - {name}" if code else name for code, name in LAN_OPTIONS] #Kod genererad med ChatGPT för att få till kortare kod än tidigare
    chosen_lan_label = st.selectbox("Välj län (valfritt)", lan_labels)    
    selected_lan = chosen_lan_label.split(" - ")[0] if " - " in chosen_lan_label else None

 

#===================== HUVUDSIDA: chat-historik =====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#===================== CHAT INPUT =====================
st.divider()
st.write("Snabbsökning")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💻 Hur ser framtiden ut för systemutvecklare?"):
        st.session_state.quick_data = {
            "query": "Hur ser framtiden ut för systemutvecklare?",
            "area": "Data/IT"  
        }
with col2:
    if st.button("📈 Hur ser framtiden ut för ekonomer?"):
        st.session_state.quick_data = {
            "query": "Hur ser framtiden ut för ekonomer?",
            "area": "Administration, ekonomi, juridik"
        }
with col3:
    if st.button("🩺 Hur ser framtiden ut för sjuksköterskor?"):
        st.session_state.quick_data = {
            "query": "Hur ser framtiden ut för sjuksköterskor?",
            "area": "Hälso- och sjukvård"
        }


if "quick_data" in st.session_state and st.session_state.quick_data:
    user_input = st.session_state.quick_data["query"]    
    selected_area = st.session_state.quick_data["area"]   
    del st.session_state.quick_data


else:
    user_input = st.chat_input("Fråga om ett yrke, t.ex. 'Hur ser framtiden ut för ekonomer?'") 
st.divider()




if user_input:
    st.session_state.api_usage += 1
    st.session_state.messages.append({"role": "user", "content": user_input})    
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyserar din fråga..."):
            try:
                response = get_chat_response(
                    message=user_input,
                    yrkesomrade=selected_area,
                    lan=selected_lan
                )
                
                analysis = response.get("analysis")
                if analysis:
                    full_response = f"{analysis['summary']}\n\n**Tips:** {analysis['recommendation']}"
                    st.markdown(full_response)
                    
                   
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                    
                    if response.get("raw_data"):
                        with st.expander("Se underlag från Yrkesbarometern"):
                            st.json(response["raw_data"])
                else:
                    st.warning("Hittade ingen data för det yrket.")
            
            except Exception as e:
                st.error(f"Ett fel uppstod: {e}")
    
    

   

