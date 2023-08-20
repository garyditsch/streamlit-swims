import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import july
from july.utils import date_range
from datetime import date, timedelta

st.title('2023 Swim Workouts')

DATE_COLUMN = 'Activity Date'
# DATA_URL = 'https://gist.githubusercontent.com/garyditsch/b2cc06fdbc2bb978639af05a1c8ac71e/raw/470416ff53d0062e2c0ac5aa71b354f86ba3e813/2023_Swims.csv'
DATA_URL = 'https://gist.githubusercontent.com/garyditsch/b2cc06fdbc2bb978639af05a1c8ac71e/raw/0869da48787e2440b084ff00758a7a915e79a3f6/2023_Swims.csv'
DATES = date_range("2023-01-01", "2023-12-31")

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(52)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

print(data.head())

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.title('Workouts grouped by time of day')
st.bar_chart(hist_values) 

# print(data[DATE_COLUMN])


# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
# st.subheader(f'Map of all pickups at {hour_to_filter}:00')
# st.map(filtered_data)

# datetest = date_range("2020-01-01", "2020-12-31")
# data2 = np.random.randint(0, 14, len(datetest))
# print(len(data2))

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

print(swim_year)
print(len(swim_year))

fig, ax = plt.subplots()

july.heatmap(DATES, 
    swim_year, 
    ax=ax,
    cmap="sunset",
    fontfamily="monospace",
    fontsize=6) 

st.title('My Swims by Day of Year')
st.pyplot(fig)
