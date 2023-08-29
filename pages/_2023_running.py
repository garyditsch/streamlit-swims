import streamlit as st
import pygwalker as pyg
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Exploring PyWalker",
    layout="wide"
)

if "df_23_runs" not in st.session_state:
   st.write('Please navigate to the home page to collect the data.')
else:  
    # Pull data from state
    df_2023_runs_sorted = st.session_state["df_23_runs"]

    # st.dataframe(df_2023_runs_sorted)

    # Generate the HTML using Pygwalker
    pyg_html = pyg.walk(df_2023_runs_sorted, return_html=True)
    
    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=1000, scrolling=True)