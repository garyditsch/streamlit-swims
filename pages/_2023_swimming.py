import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import july
from july.utils import date_range
from datetime import date, datetime, timedelta


## Start of 2023 Swim page


if "df_23_swims" not in st.session_state:
   st.write('Please navigate to the home page to collect the data.')
else:  
    # Pull data from state
    df_2023_swims_sorted = st.session_state["df_23_swims"]

    # Get some dates and times that are needed for filtering
    now = datetime.now()
    thirty_days_ago = now - timedelta(days=30)

    # A bit of legacy stuff that needs cleaned up for the calendar
    DATE_COLUMN = 'Activity Date'
    DATES = date_range("2023-01-01", "2023-12-31")


    st.title('Swim Workout Review in 2023')

    # Swim Metric Calculations
    total_swim_count = len(df_2023_swims_sorted)
    last_30_days = len(df_2023_swims_sorted[(df_2023_swims_sorted['Activity Date'].dt.tz_localize(None) >= thirty_days_ago) & (df_2023_swims_sorted['Activity Date'].dt.tz_localize(None) <= datetime.now())])

    # Metric Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Swim Count", total_swim_count)
    col2.metric("Last 30 Days", last_30_days)

    # Add Scatterplot
    fig = px.scatter(
        df_2023_swims_sorted,
        x="Activity Date",
        y="Elapsed Time",
        size_max=60,
        labels={
            "Elapsed Time": "Minutes" 
        }
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Start creating the calendar

    # Get the data
    first_date = date(2023, 1, 1)
    duration = timedelta(days=365)
    swim_year = []

    swim_dates = df_2023_swims_sorted[DATE_COLUMN].dt.strftime("%Y-%m-%d").tolist()

    for d in range(duration.days + 1):
        day = first_date + timedelta(days=d)
        if str(day) in swim_dates:
            swim_year.append(10)
        else: 
            swim_year.append(5)

    # Create figure and calendar
    fig, ax = plt.subplots()

    july.heatmap(DATES, 
        swim_year, 
        ax=ax,
        cmap="sunset",
        fontfamily="monospace",
        fontsize=6) 

    st.title('My Swims by Day of Year')
    st.pyplot(fig)


    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(df_2023_swims_sorted)

