import streamlit as st
import requests
import pandas as pd
import altair as alt
from streamlit_option_menu import option_menu
from ai_agent_jobsearch_project.frontend.constants import LAN_OPTIONS, IMG_PATH
from ai_agent_jobsearch_project.frontend.api_client import get_areas

# ===================== GRUNDKONFIGURATION =====================
st.set_page_config(layout="wide", page_title="Myndighets-Agenten")

API_ROKKA = "http://127.0.0.1:8000"   # Arbetsmarknadsinsikter
API_WENBLAD = "http://127.0.0.1:8001"  # Yrkesbarometern


# ===================== YRKESBAROMETERN =====================
def show_yrkesbarometern():
    # Session State för din del
    if "areas" not in st.session_state:
        st.session_state.areas = None
    if "messages_wb" not in st.session_state:
        st.session_state.messages_wb = []
    if "api_usage" not in st.session_state:
        st.session_state.api_usage = 0

    st.title("Yrkesbarometern")
    st.subheader("Hur ser framtiden ut för det valda yrket?")

    # --- SIDEBAR-LOGIK ---
    with st.sidebar:
        st.divider()
        st.header("Filtrera din sökning")
        
        if st.session_state.areas is None:
            try:
                st.session_state.areas = get_areas()
            except:
                st.session_state.areas = ["Data/IT"]

        selected_area = st.selectbox("Välj yrkesområde", options=st.session_state.areas)
        
        lan_labels = [f"{code} - {name}" if code else name for code, name in LAN_OPTIONS]
        chosen_lan_label = st.selectbox("Välj län (valfritt)", lan_labels)
        selected_lan = chosen_lan_label.split(" - ")[0] if " - " in chosen_lan_label else None

        if st.button("Rensa min konversation"):
            st.session_state.messages_wb = []
            st.rerun()

    # --- CHAT-HISTORIK ---
    for msg in st.session_state.messages_wb:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- SNABBSÖKNING & INPUT ---
    st.divider()
    cols = st.columns(3)
    q_data = None
    if cols[0].button("💻 Systemutvecklare"): q_data = ("Hur ser framtiden ut för systemutvecklare?", "Data/IT")
    if cols[1].button("📈 Ekonomer"): q_data = ("Hur ser framtiden ut för ekonomer?", "Administration, ekonomi, juridik")
    if cols[2].button("🩺 Sjuksköterskor"): q_data = ("Hur ser framtiden ut för sjuksköterskor?", "Hälso- och sjukvård")

    user_input = st.chat_input("Fråga om ett yrke...")
    
    final_input = q_data[0] if q_data else user_input
    final_area = q_data[1] if q_data else selected_area

    if final_input:
        st.session_state.api_usage += 1
        st.session_state.messages_wb.append({"role": "user", "content": final_input})
        with st.chat_message("user"): st.markdown(final_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyserar..."):
                try:
                    payload = {"yrkesomrade": final_area, "message": final_input, "lan": selected_lan}
                    response = requests.post(f"{API_WENBLAD}/chat", json=payload).json()
                    analysis = response.get("analysis")
                    if analysis:
                        full_res = f"{analysis['summary']}\n\n**Tips:** {analysis['recommendation']}"
                        st.markdown(full_res)
                        st.session_state.messages_wb.append({"role": "assistant", "content": full_res})
                        if response.get("raw_data"):
                            with st.expander("Se underlag"): st.json(response["raw_data"])
                    else:
                        st.warning("Ingen data hittades.")
                except Exception as e:
                    st.error(f"Kunde inte nå din backend på 8001: {e}")

# ===================== Arbetsmarknadsinsikter =====================
def show_home():
    st.image(str(IMG_PATH), width=500)
    st.title("Fråga en myndighet")
    st.write("Välkommen! Välj en tjänst i menyn till vänster för att komma igång.")

def show_job_insights():
    st.title("Arbetsmarknadsinsikter")
    st.subheader("Jämför sökintresse vs. jobbannonser")

    days = st.slider("Dagar", 1, 7, 14)
    acol1, acol2 = st.columns([1.4, 1.4], gap="large")

    # Topp sökningar
    with acol1:
        st.markdown("### Topp 10 sökta jobb")
        try:
            data = requests.get(f"{API_ROKKA}/top-searches", params={"days": days}).json()
            df = pd.DataFrame(data)
            if not df.empty:
                chart = alt.Chart(df).mark_bar(cornerRadius=6).encode(
                    x="count:Q", y=alt.Y("label:N", sort="-x"), tooltip=["label", "count"]
                ).properties(height=420)
                st.altair_chart(chart, use_container_width=True)
            else: st.info("Ingen sökdata.")
        except: st.error("Kunde inte nå kompisens API (8000)")

    # Topp annonser
    with acol2:
        st.markdown("### Topp 10 annonserade jobb")
        try:
            data = requests.get(f"{API_ROKKA}/top-job-listings", params={"days": days}).json()
            df = pd.DataFrame(data)
            if not df.empty:
                chart = alt.Chart(df).mark_bar(cornerRadius=6).encode(
                    x="count:Q", y=alt.Y("label:N", sort="-x"), tooltip=["label", "count"]
                ).properties(height=420)
                st.altair_chart(chart, use_container_width=True)
            else: st.info("Ingen annonsdata.")
        except: st.error("Kunde inte nå kompisens API (8000)")

    st.markdown("# Jobbsökarens agent")
    text_input = st.text_input(label="Fråga agenten om jobbannonser:")
    if st.button("Send") and text_input.strip():
        try:
            resp = requests.post(f"{API_ROKKA}/rag/query", json={"prompt": text_input})
            if resp.status_code == 200:
                res_data = resp.json()
                st.markdown(f"**Svar:** {res_data['answer']}")
                st.caption(f"Källa: {res_data['occupation_group']}")
        except: st.error("Kunde inte nå RAG-agenten på port 8000")

# ===================== GEMENSAM MENY OCH ROUTER =====================
with st.sidebar:
    selected = option_menu(
        menu_title="Välj flik",
        options=["Hem", "Yrkesbarometern", "Arbetsmarknadsinsikter"],
        icons=["house", "clock", "graph-up-arrow"],
        menu_icon="chat-left-text",
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": "#002147", "color": "white"},
        }
    )

if selected == "Arbetsmarknadsinsikter":
    show_job_insights()
elif selected == "Yrkesbarometern":
    show_yrkesbarometern()
else:
    show_home()