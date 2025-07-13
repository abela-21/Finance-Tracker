import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import json

st.set_page_config(layout="wide")

st.title("Market and Competitive Intelligence Dashboard")

# --- User Inputs ---
st.sidebar.header("Controls")
tickers_input = st.sidebar.text_input("Enter Tickers (comma-separated)", "BEF.SG,AUR.AX")
days_input = st.sidebar.slider("Select Days", 1, 365, 30)

if st.sidebar.button("Run Analysis"):
    if not tickers_input:
        st.error("Please enter at least one ticker.")
    else:
        with st.spinner("Fetching data and running analysis..."):
            try:
                # Call the backend API
                response = requests.post(
                    "http://127.0.0.1:8000/competitive_analysis",
                    json={"tickers": [t.strip() for t in tickers_input.split(',')], "days": days_input}
                )
                response.raise_for_status()

                api_data = response.json()

                # Store data in session state to persist it
                st.session_state['api_data'] = api_data
                st.session_state['tickers'] = tickers_input

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend: {e}")
                st.session_state['api_data'] = None

# --- Display Results ---
if 'api_data' in st.session_state and st.session_state['api_data']:
    api_data = st.session_state['api_data']

    # Display Plotly Chart
    st.header("Stock Price Trend")
    chart_data = json.loads(api_data['chart'])
    st.plotly_chart(go.Figure(chart_data), use_container_width=True)

    # Display Benchmark Summary
    st.header("Benchmark Summary")
    benchmark_df = pd.DataFrame(api_data['benchmark']).T
    st.dataframe(benchmark_df.style.format("{:.2f}"))

    # Download Report Button
    st.header("Download Report")
    report_filename = api_data['report_filename']

    try:
        with open(report_filename, "r") as f:
            st.download_button(
                label="Download HTML Report",
                data=f.read(),
                file_name=report_filename,
                mime="text/html"
            )
    except FileNotFoundError:
        st.warning(f"Report file '{report_filename}' not found. Please ensure the backend generated it.")
else:
    st.info("Enter tickers and click 'Run Analysis' to see the results.")
