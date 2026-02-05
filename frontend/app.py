import streamlit as st
import requests
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

API = "http://127.0.0.1:8000"

st.title("Job market insights")
st.subheader("Comparing search interest vs. posted job ads")

days = st.slider("Days", 1, 7, 14)

col1, col2 = st.columns(2)

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


with col1:
    st.markdown("### Top searched jobs")
    data = requests.get(f"{API}/top-searches", params={"days": days}).json()
    df_searches = pd.DataFrame(data)

    if df_searches.empty:
        st.info("No search data returned from API")
    else:
        df_searches["label"] = df_searches["label"].astype(str)
        df_searches["count"] = pd.to_numeric(df_searches["count"], errors="coerce").fillna(0).astype(int)
        df_searches = df_searches.sort_values("count", ascending=True)

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

        st.altair_chart(chart, use_container_width=True)