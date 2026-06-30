from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_synthetic_data.csv"

st.set_page_config(page_title="AI Job Search Automation Dashboard", layout="wide")
st.title("AI Job Search Automation Dashboard")
st.caption("Synthetic pipeline data. This is not Juan's real application history.")

df = pd.read_csv(DATA_PATH, parse_dates=["date", "follow_up_due"])
role = st.selectbox("Role family", ["All"] + sorted(df["role_family"].unique()))
if role != "All":
    df = df[df["role_family"] == role]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Applications", len(df))
c2.metric("Avg fit score", f"{df['fit_score'].mean():.1f}")
c3.metric("Response rate", f"{df['response_received'].mean() * 100:.1f}%")
c4.metric("Active interviews", int((df["status"] == "Interview").sum()))

st.subheader("Status funnel")
st.bar_chart(df["status"].value_counts())

st.subheader("Applications over time")
by_day = df.groupby("date").size().rename("applications")
st.line_chart(by_day)

st.subheader("Pipeline table")
st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
