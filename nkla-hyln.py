import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import csv
from array import array
import dateparser

st.subheader("Hyliion/Nikola Stock Ratio (%)")

result_count = st.slider('Days to count from', 10, 400, 150)

hyln_data_read = []
with open('hyliion_data.csv') as file:
    hyln_data = csv.reader(file)
    for row in hyln_data:
        hyln_data_read.append(row)

hyln_results = hyln_data_read[1:]
hyln_results = hyln_results[-result_count:]

hyln_closes = [float(i) for i in np.array(hyln_results)[:, 3]]

dates = np.array(hyln_results)[:, 0]
dates = [dateparser.parse(d) for d in dates]

nkla_data_read = []
with open('nikola_data.csv') as file:
    nkla_data = csv.reader(file)
    for row in nkla_data:
        nkla_data_read.append(row)

nkla_results = nkla_data_read[-result_count:]

nkla_closes = [float(i) for i in np.array(nkla_results)[:, 3]]

stock_ratio = []

for index in range(result_count):
    ratio = hyln_closes[index] / nkla_closes[index]
    stock_ratio.append(ratio * 100)


source = pd.DataFrame({
  'Date': dates,
  'Ratio (%)': stock_ratio
})

c = alt.Chart(source).mark_line().encode(
    x='Date',
    y='Ratio (%)'
)

st.altair_chart(c, use_container_width=True)


datas = [[dates[i], stock_ratio[i], hyln_closes[i], nkla_closes[i]] for i in range(result_count)]

source = pd.DataFrame(datas,columns=['Date', 'ratio (%)', 'Stock Price', 'nkla'])

base = alt.Chart(source).encode(x=alt.X('Date', axis=alt.Axis(labelAngle=-45, tickCount=10)))


st.subheader("Hyliion and Nikola Stock Price")

stock_prices_chart = alt.layer(base.mark_line(color='green').encode(y='Stock Price'))

if st.checkbox('Show NKLA stock price'):
    stock_prices_chart = alt.layer(
        base.mark_line(color='blue').encode(y=alt.Y('nkla', title='Stock Price')),
        base.mark_line(color='green').encode(y='Stock Price'))

st.altair_chart(stock_prices_chart, use_container_width=True)

# ratio_chart = alt.layer(
#     base.mark_line(color='orange').encode(y='ratio (%)')
# ).interactive()

# st.altair_chart(ratio_chart, use_container_width=True)
