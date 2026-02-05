from urllib import response
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from ai_agent_jobsearch_project.frontend.constants import IMG_PATH

API_ROKKA = "http://127.0.0.1:8000"

st.set_page_config(layout="wide") #more space, wider page

def show_home():
    st.image(str(IMG_PATH),width=500)
    st.title("Fråga en myndighet")


def show_job_insights():             

    st.title("Arbetsmarknadsinsikter")
    st.subheader("Jämför sökintresse vs. jobbannonser")

    days = st.slider("Dagar", 1, 7, 14)


    #--- 'altair' chart tip from streamlit.io
    #-----Altair charts -------
    acol1, acol2 = st.columns([1.4, 1.4], gap="large")

    with acol1:
        st.markdown("### Topp 10 sökta jobb")
        data = requests.get(f"{API_ROKKA}/top-searches", params={"days": days}).json()
        df_searches = pd.DataFrame(data)

        if df_searches.empty:
            st.info("No search data returned from API")
        else:
            df_searches["label"] = df_searches["label"].astype(str)
            df_searches["count"] = pd.to_numeric(df_searches["count"], errors="coerce").fillna(0).astype(int)
            df_searches = df_searches.sort_values("count", ascending=True)

            # added validation for pyArrow
            records = df_searches[["label", "count"]].to_dict("records")

            chart = (
                alt.Chart(alt.Data(values=records))
                .mark_bar(cornerRadius=6)
                .encode(
                    x=alt.X("count:Q", title="Search Count"),
                    y=alt.Y("label:N", sort="-x", title=None, axis=alt.Axis(labelLimit=260, labelPadding=10)),
                    tooltip=[alt.Tooltip("label:N"), alt.Tooltip("count:Q")],
                )
                .properties(title=f"Flest sökningar (senaste {days} dagarna)", height = 420,)
            )

            st.altair_chart(chart, width="stretch")

    with acol2:
        st.markdown("### Topp 10 annonserade jobb")
        data = requests.get(f"{API_ROKKA}/top-job-listings", params={"days": days}).json()
        df_jobs = pd.DataFrame(data)

        if df_jobs.empty:
            st.info("No job ads data returned from API.")
        else:
            df_jobs["label"] = df_jobs["label"].astype(str)
            df_jobs["count"] = pd.to_numeric(df_jobs["count"], errors="coerce").fillna(0).astype(int)

            records = df_jobs[["label", "count"]].to_dict("records")

            chart = (
                alt.Chart(alt.Data(values=records))
                .mark_bar(cornerRadius=6)
                .encode(
                    x=alt.X("count:Q", title="Job Ads Count"),
                    y=alt.Y("label:N", sort="-x", title=None, axis=alt.Axis(labelLimit=260, labelPadding=10)),
                    tooltip=[alt.Tooltip("label:N"), alt.Tooltip("count:Q")],
                )
                .properties(title=f"Flest sökta jobb (senaste {days} dagarna)", height= 420,)
            )

            st.altair_chart(chart, width="stretch") 

    # --------RAG agent for querying job ads -------
    # ------ code inspired by school code-alongs repo -------

    st.markdown("# Jobbsökarens agent")
    st.markdown("### Fråga mig vad som krävs i arbetslivet")
    st.markdown("Jag svarar på frågor om de topp 10 annonserade jobben och vilka kunskaper du behöver ha som kandidat")
    text_input = st.text_input(label="Skriv något:")

    if st.button("Send") and text_input.strip() != "":
        response = requests.post(
                "http://127.0.0.1:8000/rag/query", json={"prompt": text_input}
            )
        # validation
        if response.status_code != 200:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)
                st.stop()
        data = response.json()

        st.markdown("## Fråga:")
        st.markdown(text_input)

        st.markdown("## Svar:")
        st.markdown(data["answer"])

        st.markdown("## Source:")
        st.markdown(data["occupation_group"])


# --- Side menu for option_menu for selecting yrkesbarometern or arbetsmarknadsinsikter ------#
with st.sidebar:
    selected = option_menu(
        menu_title="Välj flik",
        options=["Hem", "Yrkesbarometern", "Arbetsmarknadsinsikter"],
        icons=["house", "clock", "graph-up-arrow"],
        menu_icon="chat-left-text",
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "inherit", "font-size": "20px"},  # marinblå ikon
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "color": "black",
                "--hover-color": "#e6e9ef"
            },
            "nav-link-selected": {
                "background-color": "#002147",  # marinblå bakgrund för aktivt val
                "color": "white"                # vit text
            },
        }
    )



# --- router for main page selector ------
if selected == "Arbetsmarknadsinsikter":
    show_job_insights()
elif selected == "Yrkesbarometern":
#    show_barometer():
#else:
    show_home()






# to run streamlit frontend:
# uv run streamlit run src/ai_agent_jobsearch_project/frontend/app.py