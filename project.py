import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon


df = pd.read_csv("ilidata.csv")


st.title("Ilodigwe ILI Surveillance Visualization")
st.markdown("This app displays influenza illness trends by state and models ILI percentages usin exponential distribution.")

states = df['state'].dropna().unique()
states.sort()
selected_state = st.selectbox("Select a state", states)

state_data = df[df['state'] == selected_state].copy()
state_data = state_data.sort_values("epiweek")
state_data['weeks'] = range(len(state_data))

# Section: Time Series Line Chart
st.header(f"Time Series of ILI % for {selected_state}") #f string 
st.line_chart(state_data[['weeks', 'ili']].set_index('weeks'))

# Section: Histogram with Exponential Overlay
st.header("Dist. of ILI % with Exponential Fit")

ili_values = state_data['ili'].dropna()
lambda_hat = 1 / np.mean(ili_values)

x_vals = np.linspace(0, ili_values.max(), 100)
pdf_vals = expon(scale=1/lambda_hat).pdf(x_vals)

fig, ax = plt.subplots()
ax.hist(ili_values, bins=20, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='ILI % Histogram')
ax.plot(x_vals, pdf_vals, 'r-', label=f'Exponential Fit\nλ ≈ {lambda_hat:.2f}')
ax.set_xlabel("ILI Percentage")
ax.set_ylabel("Density")
ax.set_title("Histogram of ILI % with Exponential Fit")
ax.legend()
st.pyplot(fig)


st.header("Interpretation")
st.markdown("""
Interpretations of visualizations:

1. **ILI Time Series:** The line chart or first plot above tracks how the ILI percentage (`ili`) changes over epidemiological weeks for the selected state in the drop down menu. shows the weekly progression of the ILI percentage across the full duration of the dataset for the selected state. 
    This time series view highlights potential recurring spikes and seasonal trends in flu-like symptoms over time based on the data provided to us.
    It enables public health analysts to identify patterns, such as winter peaks or abnormalities, that may indicate differing flu activity in a given season.

2. **ILI Distribution Fit:** The histogram below shows the distribution of ILI percentages over all weeks for the state of choice. 
    To analyze the statistical distribution of ILI observations, we overlay a fitted exponential distribution (`This is under the assumption the values are drawn from the Exponential distribution.`). 
    The exponential model is based on the Law of Large Numbers, which suggests that the avg of many independent ILI values will approximate the expected value or mean. 
    By estimating the rate parameter lambda as the reciprocal of the sample mean, we generate a curve that approximates the distribution of observed ILI values. 
    Our visualization helps us assess any potential patterns in the occurrence of flu illness over time.
 



Together, these visualizations provide both time-based and distributional insight into how ILI behaves across seasons and regions (`states in our case`).

As expected from the Law of Large Numbers, the sample average of these ILI observations converges to the true expected value as more data is collected.
""")
