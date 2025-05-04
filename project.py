import streamlit as st
import pandas as pd

# Load the ILI dataset
df = pd.read_csv("ilidata.csv")

# Create a list of unique states from the data
states = df['state'].dropna().unique()
states.sort()

# Sidebar selection
selected_state = st.selectbox("Select a state", states)

# Filter the data for the selected state
state_data = df[df['state'] == selected_state].copy()
state_data = state_data.sort_values('epiweek')  # Make sure it's in time order

# Create a 'weeks' column (0 to N-1 for plotting x-axis)
state_data['weeks'] = range(len(state_data))

# Plot line chart of unweighted ILI %
st.line_chart(state_data[['weeks', 'ili']].set_index('weeks'), use_container_width=True)
