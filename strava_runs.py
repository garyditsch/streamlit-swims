import streamlit as st
import pandas as pd
from pyairtable import Api
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import july
from july.utils import date_range
from datetime import date, timedelta

api = Api(st.secrets["AIRTABLE_API_KEY"])
table = api.table('appAsWd4GyI8WrvPk', 'tblENY9sFTGYzvc0u')
activities = table.all()
strava_data = [item['fields'] for item in activities]
df = pd.DataFrame(strava_data)
df['Activity Date'] = pd.to_datetime(df['Activity Date'])
df_2023 = df[(df['Activity Date'] > "2022-12-31")]
df_2023_swims = df_2023[(df_2023['Activity Type'] == 'Swim')]
df_sorted = df_2023_swims.sort_values(by='Activity Date', ascending=False)
df_sorted['Elapsed Time'] = df_sorted['Elapsed Time'].div(60).round(2)
df_sorted_minutes = df_sorted[['Elapsed Time', 'Day of Year', 'Activity Date']]

st.title('2023 Swim Workouts')

DATE_COLUMN = 'Activity Date'
DATES = date_range("2023-01-01", "2023-12-31")

@st.cache_data
def load_data(nrows):
    data = df_sorted[0:nrows]
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
data = load_data(60)
data_load_state.text("Data has loaded.")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

fig = px.scatter(
    df_sorted,
    x="Activity Date",
    y="Elapsed Time",
    size_max=60,
    labels={
        "Elapsed Time": "Minutes" 
    }
)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)

first_date = date(2023, 1, 1)
duration = timedelta(days=365)
swim_year = []

swim_dates = data[DATE_COLUMN].dt.strftime("%Y-%m-%d").tolist()

for d in range(duration.days + 1):
    day = first_date + timedelta(days=d)
    if str(day) in swim_dates:
        swim_year.append(10)
    else: 
        swim_year.append(5)

fig, ax = plt.subplots()

july.heatmap(DATES, 
    swim_year, 
    ax=ax,
    cmap="sunset",
    fontfamily="monospace",
    fontsize=6) 

st.title('My Swims by Day of Year')
st.pyplot(fig)
