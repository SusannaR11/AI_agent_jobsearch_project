import streamlit as st
import requests
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

API = "http://127.0.0.1:8000"

st.set_page_config(layout="wide") #more space, wider page

st.title("Job market insights")
st.subheader("Comparing search interest vs. posted job ads")

days = st.slider("Days", 1, 7, 14)

col1, col2 = st.columns([1, 1], gap="large")

#---- left column -------
#--- 'altair' chart tip from streamlit.io
with col1: 
    st.markdown("### Top searched jobs") 
    data = requests.get(f"{API}/top-searches", params={"days": days}).json() 
    df_searches = pd.DataFrame(data) 
    #validation if no search data from API 
    if df_searches.empty: 
        st.info("No search data returned from API") 
    else: 
        fig = plt.figure() 
        df_searches = df_searches.sort_values("count") 
        plt.barh(df_searches["label"], df_searches["count"]) 
        plt.title(f"Top searches (last {days} days)") 
        plt.tight_layout() 
        st.pyplot(fig)

#-----right column -------
with col2:
    st.subheader("Top advertised jobs")
    data = requests.get(f"{API}/top-job-listings", params={"days": days}).json()

    df_jobs = pd.DataFrame(data)

    # validation if empty
    if df_jobs.empty:
        st.info("No job ads data returned from API.")
    else:
        fig = plt.figure()
        df_jobs = df_jobs.sort_values("count")
        plt.barh(df_jobs["label"], df_jobs["count"])
        plt.title(f"Top job ads (last {days} days)")
        plt.tight_layout()
        st.pyplot(fig)


# to run streamlit frontend:
# uv run streamlit run frontend/app.py

#-----Altair tester
acol1, acol2 = st.columns([1.3, 1.3], gap="large")

with acol1:
    st.markdown("### Top searched jobs")
    data = requests.get(f"{API}/top-searches", params={"days": days}).json()
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
                y=alt.Y("label:N", sort="-x", title="Job Title"),
                tooltip=[alt.Tooltip("label:N"), alt.Tooltip("count:Q")],
            )
            .properties(title=f"Top searches (last {days} days)")
        )

        st.altair_chart(chart, width="stretch")

with acol2:
    st.markdown("### Top advertised jobs")
    data = requests.get(f"{API}/top-job-listings", params={"days": days}).json()
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
                y=alt.Y("label:N", sort="-x", title="Job Title"),
                tooltip=[alt.Tooltip("label:N"), alt.Tooltip("count:Q")],
            )
            .properties(title=f"Top job ads (last {days} days)")
        )

        st.altair_chart(chart, width="stretch") 

# --------RAG agent for querying job ads -------
# ------ code inspired by school code-alongs repo -------

def layout():

    st.markdown("# Jobsökarens agent")
    st.markdown("Fråga mig om vad som krävs i arbetslivet")
    text_input = st.text_input(label="Fråga mig")

    if st.button("Send") and text_input.strip() != "":
        response = requests.post(
            "http://127.0.0.1:8000/rag/query", json={"prompt": text_input}
        )

        data = response.json()

        st.markdown("## Fråga:")
        st.markdown(text_input)

        st.markdown("## Svar:")
        st.markdown(data["answer"])

        st.markdown("## Source:")
        st.markdown(data["occupation_group"])


if __name__ == "__main__":
    layout()

