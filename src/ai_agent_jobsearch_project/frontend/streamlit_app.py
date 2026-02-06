# import streamlit as st
# import requests
# from ai_agent_jobsearch_project.frontend.constants import LAN_OPTIONS
# from ai_agent_jobsearch_project.frontend.api_client import get_areas


# API_WENBLAD = "http://127.0.0.1:8001"

# def show_yrkesbarometern():
#     # ===================== Initiera Session State =====================

#     if "areas" not in st.session_state:
#         st.session_state.areas = None
#     if "messages_wb" not in st.session_state:
#         st.session_state.messages_wb = []
#     if "api_usage" not in st.session_state:
#         st.session_state.api_usage = 0

#     # ===================== Sidomeny (Filter) =====================
#     with st.sidebar:
#         st.header("Filtrera din sökning")
        
#         # Ladda områden om de inte finns
#         if st.session_state.areas is None:
#             try:
#                 st.session_state.areas = get_areas()
#             except:
#                 st.session_state.areas = ["Data/IT"]

#         selected_area = st.selectbox("Välj yrkesområde", options=st.session_state.areas)
        
#         lan_labels = [f"{code} - {name}" if code else name for code, name in LAN_OPTIONS]
#         chosen_lan_label = st.selectbox("Välj län (valfritt)", lan_labels)
#         selected_lan = chosen_lan_label.split(" - ")[0] if " - " in chosen_lan_label else None

#         # API Monitor & Rensa-knapp
#         with st.expander("Systemstatus"):
#             st.progress(min(st.session_state.api_usage / 15, 1.0))
#             st.caption(f"API-anrop: {st.session_state.api_usage}/15")
#             if st.button("Rensa konversation"):
#                 st.session_state.messages_wb = []
#                 st.rerun()

#     # ===================== Huvudsida =====================
#     st.title("Yrkesbarometern")
#     st.subheader("Hur ser framtiden ut för ditt drömyrke?")

#     # Visa chatthistorik
#     for msg in st.session_state.messages_wb:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # Snabbsökning (Knappar)
#     st.write("Snabbsökning")
#     cols = st.columns(3)
#     quick_queries = [
#         ("💻 Systemutvecklare", "Hur ser framtiden ut för systemutvecklare?", "Data/IT"),
#         ("📈 Ekonomer", "Hur ser framtiden ut för ekonomer?", "Administration, ekonomi, juridik"),
#         ("🩺 Sjuksköterskor", "Hur ser framtiden ut för sjuksköterskor?", "Hälso- och sjukvård")
#     ]

#     clicked_query = None
#     for i, (label, query, area) in enumerate(quick_queries):
#         if cols[i].button(label):
#             clicked_query = (query, area)

#     # Chat input
#     user_input = st.chat_input("Fråga om ett yrke...")
    
#     # Hantera input (antingen från knapp eller textfält)
#     final_input = None
#     final_area = selected_area

#     if clicked_query:
#         final_input, final_area = clicked_query
#     elif user_input:
#         final_input = user_input

#     if final_input:
#         st.session_state.api_usage += 1
#         st.session_state.messages_wb.append({"role": "user", "content": final_input})
        
#         with st.chat_message("user"):
#             st.markdown(final_input)

#         with st.chat_message("assistant"):
#             with st.spinner("Analyserar..."):
#                 try:
#                     payload = {"yrkesomrade": final_area, "message": final_input, "lan": selected_lan}
#                     # Anropa backend på port 8001
#                     response = requests.post(f"{API_WENBLAD}/chat", json=payload).json()
                    
#                     analysis = response.get("analysis")
#                     if analysis:
#                         full_res = f"{analysis['summary']}\n\n**Tips:** {analysis['recommendation']}"
#                         st.markdown(full_res)
#                         st.session_state.messages_wb.append({"role": "assistant", "content": full_res})
                        
#                         if response.get("raw_data"):
#                             with st.expander("Se underlag"):
#                                 st.json(response["raw_data"])
#                     else:
#                         st.warning("Hittade ingen data.")
#                 except Exception as e:
#                     st.error(f"Fel: {e}")