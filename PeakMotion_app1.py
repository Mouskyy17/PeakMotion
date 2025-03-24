import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("CFC Physical Capability Data_.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
movement = st.sidebar.selectbox("Select Movement", df["MOVEMENT"].unique())
quality = st.sidebar.selectbox("Select Quality", df["QUALITY"].unique())
expression = st.sidebar.selectbox("Select Expression", df["EXPRESSION"].unique())

# Filter data
df_filtered = df[(df["MOVEMENT"] == movement) & (df["QUALITY"] == quality) & (df["EXPRESSION"] == expression)]

# Title
st.title("Football Player Physical Performance Dashboard")

# Line chart of performance over time
st.subheader(f"Performance Trend for {movement} - {quality} - {expression}")
fig = px.line(df_filtered, x="Date", y="Score", title="Performance Score Over Time")
st.plotly_chart(fig)

# Benchmark comparison
if "BenchmarkPct" in df_filtered.columns:
    st.subheader("Benchmark Comparison")
    fig_bench = px.line(df_filtered, x="Date", y="BenchmarkPct", title="Benchmark Percentage Over Time")
    st.plotly_chart(fig_bench)

# Show data table
st.subheader("Raw Data")
st.dataframe(df_filtered)
