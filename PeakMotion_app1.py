import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    file_path = "/mnt/data/CFC Physical Capability Data_.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

df["Date"] = pd.to_datetime(df["Date"])

# Sidebar filters
st.sidebar.header("Filters")
movement = st.sidebar.selectbox("Select Movement", df["MOVEMENT"].unique())
quality_options = st.sidebar.multiselect("Select Quality", df["QUALITY"].unique(), default=df["QUALITY"].unique()[0])
expression_options = st.sidebar.multiselect("Select Expression", df["EXPRESSION"].unique(), default=df["EXPRESSION"].unique()[0])

# Filter data
df_filtered = df[(df["MOVEMENT"] == movement) & (df["QUALITY"].isin(quality_options)) & (df["EXPRESSION"].isin(expression_options))]

# Title
st.title("Football Player Physical Performance Dashboard")

# Line chart of performance over time
st.subheader(f"Performance Trend for {movement}")
fig = px.line(df_filtered, x="Date", y="Score", color="QUALITY", title="Performance Score Over Time")
st.plotly_chart(fig)

# Benchmark comparison
if "BenchmarkPct" in df_filtered.columns:
    st.subheader("Benchmark Comparison")
    fig_bench = px.line(df_filtered, x="Date", y="BenchmarkPct", color="QUALITY", title="Benchmark Percentage Over Time")
    st.plotly_chart(fig_bench)

# Heatmap of performance trends
st.subheader("Performance Heatmap")
heatmap_data = df.pivot_table(index="QUALITY", columns="Date", values="Score", aggfunc="mean")
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="coolwarm", linewidths=0.5)
st.pyplot(plt)

# Detect performance peaks and drops
st.subheader("Performance Peaks & Drops")
df_filtered["Score_Diff"] = df_filtered["Score"].diff()
df_peaks = df_filtered[df_filtered["Score_Diff"] > df_filtered["Score_Diff"].quantile(0.95)]
df_drops = df_filtered[df_filtered["Score_Diff"] < df_filtered["Score_Diff"].quantile(0.05)]
st.write("### Performance Peaks")
st.dataframe(df_peaks)
st.write("### Performance Drops")
st.dataframe(df_drops)

# Correlation between qualities
st.subheader("Correlation Between Qualities")
corr_matrix = df.pivot_table(index="Date", columns="QUALITY", values="Score", aggfunc="mean").corr()
plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
st.pyplot(plt)

# Show data table
st.subheader("Raw Data")
st.dataframe(df_filtered)
