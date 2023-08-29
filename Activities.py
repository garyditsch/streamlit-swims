import streamlit as st
import pandas as pd
from pyairtable import Api
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import july
from july.utils import date_range
from datetime import date, datetime, timedelta

# Get the data from Airtable 
@st.cache_data
def get_airtable_data(appId, tableId):
    api = Api(st.secrets["AIRTABLE_API_KEY"])
    table = api.table(appId, tableId)
    data = table.all()
    return data

activities = get_airtable_data('appAsWd4GyI8WrvPk', 'tblENY9sFTGYzvc0u')

# Flatten the data and put into a pandas dataframe
strava_data = [item['fields'] for item in activities]
df = pd.DataFrame(strava_data)

# Convert date column to pandas datetime
df['Activity Date'] = pd.to_datetime(df['Activity Date'])

# Convert Elapsed Time column to minutes and round to 2 decimals
df['Elapsed Time'] = df['Elapsed Time'].div(60).round(2)

total_runs = df[(df['Activity Type'] == 'Run')] 
total_swim = df[(df['Activity Type'] == 'Swim')] 
total_bike = df[(df['Activity Type'] == 'Ride')] 

# Function to filter df based on start & end activity dates

@st.cache_data
def get_date_filtered_df(data, start, end):
    filtered_frame = data[(data['Activity Date'] >= start) & (data['Activity Date'] <= end)]
    return filtered_frame

# Get dataframe of only 2023 swim activities
df_2023_swims = get_date_filtered_df(total_swim, "2023-01-01", "2023-12-31")

# Get swim workouts and sort by date
df_2023_swims_sorted = df_2023_swims.sort_values(by='Activity Date', ascending=False)

# Get dataframe of only 2023 run activities
df_2023_runs = get_date_filtered_df(total_runs, "2023-01-01", "2023-12-31")

# Get run workouts and sort by date
df_2023_runs_sorted = df_2023_runs.sort_values(by='Activity Date', ascending=False)

if "df_23_swims" not in st.session_state:
   st.session_state["df_23_swims"] = df_2023_swims_sorted

if "df_23_runs" not in st.session_state:
    st.session_state["df_23_runs"] = df_2023_runs_sorted

first_workout = min(df['Activity Date'])
first_workout_formatted = first_workout.strftime('%m/%d/%Y')
last_workout = max(df['Activity Date'])
last_workout_formatted = last_workout.strftime('%m/%d/%Y')

total_run_mins = (total_runs['Elapsed Time'].sum() / 60).round(2)
total_swim_mins = (total_swim['Elapsed Time'].sum() / 60).round(2)
total_bike_mins = (total_bike['Elapsed Time'].sum() / 60).round(2)

# Metric Row
col1, col2 = st.columns(2)
col1.metric("First Workout", first_workout_formatted)
col2.metric("Most Recent Workout", last_workout_formatted)

# Metric Row
col1, col2, col3 = st.columns(3)
col1.metric("Total Hours of Running", total_run_mins)
col2.metric("Total Hours of Swimming", total_swim_mins)
col3.metric("Total Hours of Biking", total_bike_mins)