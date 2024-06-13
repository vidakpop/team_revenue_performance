import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
import altair as alt
import time
import base64
from streamlit_lottie import st_lottie

# Set page configuration
st.set_page_config(
    page_title='Team Performance Revenue Analysis',
    page_icon=':bar_chart:',
    layout='wide'
)

# Function to fetch JSON data
def get(path: str):
    with open(path, "r") as p:
        return json.load(p)

# Fetch path for Lottie animation from app.json
path = get('app.json')

# Create a placeholder for the preloader
preloader_placeholder = st.empty()

# Show the preloader with the welcome text and animation
with preloader_placeholder.container():
    with st.spinner('Welcome to our Analytics app! Loading...'):
        st_lottie(path)  # Display Lottie animation
        time.sleep(4)  # Simulate a delay to mimic loading time

# Clear the preloader after loading is complete
preloader_placeholder.empty()

# Set dark mode theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load dataset
df = pd.read_csv('revenue_3(1).csv')

# Function to load and display logo
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to logo image
logo_path = "logo.png"
logo_base64 = get_image_base64(logo_path)

# Display logo centered
st.markdown(
    f"""
    <style>
    .container {{
        display: flex;
        justify-content: center;
    }}
    </style>
    <div class="container">
        <img src="data:image/png;base64,{logo_base64}" alt="logo" width="200">
    </div>
    """,
    unsafe_allow_html=True
)

# Directorate header
st.markdown(
    "<div style='background:'black''><h1 style='color:#ac2217;display:flex;justify-content: center'>DIRECTORATE OF LICENSING AND COMPLIANCE</h1></div>",
    unsafe_allow_html=True
)

# Main title
st.title(':bar_chart: Team Performance Revenue Analysis')

# Sidebar setup
st.sidebar.title('Revenue Team Analysis')
total_revenue = df['TOTAL'].sum()
st.sidebar.subheader('Total Revenue Collected:')
st.sidebar.markdown(f'Kshs. {total_revenue:,.0f}')

# Rank teams by their total revenue
df_rank = df.sort_values(by='TOTAL', ascending=False).reset_index(drop=True)
df_rank['RANK'] = df_rank.index + 1

# Display team rankings in the sidebar
st.sidebar.subheader('Team Ranking:')
num_teams = len(df_rank)
for index, row in df_rank.iterrows():
    stars = ':star:' * (num_teams - row['RANK'] + 1)  # Create stars based on rank
    st.sidebar.write(f"{row['TEAMS']}: {stars}")

# Team selection dropdown
teams = st.sidebar.multiselect(
    'Select Team:',
    options=df['TEAMS'].unique(),
    default=df['TEAMS'].unique()
)

# Filter dataframe based on selected teams
df_selection = df.query('TEAMS==@teams')

# Display selected data
st.dataframe(df_selection)

# Main panel for team selection
with st.expander("Team Selection", expanded=True):
    team = st.selectbox('Select Team:', options=teams)
    if team == 'All Teams':
        st.dataframe(df)
    else:
        team_df = df[df['TEAMS'] == team]
        st.dataframe(team_df)

# First chart column setup
chart1, chart2 = st.columns([1, 2])

with chart1:
    # Create a bar chart for team distribution ranking
    team_totals = df.groupby('TEAMS')['TOTAL'].sum().reset_index()
    pie_chart = alt.Chart(team_totals).mark_bar().encode(
        alt.X('TOTAL:Q', axis=None),
        alt.Y('TEAMS:O', sort='-x'),
        color=alt.Color('TEAMS:N', legend=None)
    ).properties(
        title='Team Distribution Ranking'
    )
    st.altair_chart(pie_chart, use_container_width=True)

with chart2:
    # Create a cumulative revenue trend bar chart
    c = alt.Chart(df).mark_bar().encode(
        x='TEAMS',
        y='TOTAL',
        color='TEAMS',
        tooltip=['27/05/2024', '28/05/2024', '29/05/2024', '30/05/2024', '31/05/2024'],
    ).properties(
        title="Cumulative Revenue Trend by Teams",
    ).interactive()

    # Add text for the grand total
    grand_total = df['TOTAL'].sum()
    text = alt.Chart(pd.DataFrame({'Grand Total': [grand_total]})).mark_text(
        align='center',
        baseline='middle',
        fontSize=14,
        color='white',
        dx=50,  # adjust text position
        dy=-50,  # adjust text position
    ).encode(
        text='Grand Total'
    )
    chart2 = c + text
    st.altair_chart(chart2, use_container_width=True)

# Panel for stacked bar chart
with st.expander("Stacked Bar Chart", expanded=True):
    # Melt the DataFrame to long format for daily data
    df_melted = df.melt(id_vars=["TEAMS", "TOTAL"], var_name="Date", value_name="Amount")

    # Stacked bar chart
    stacked_bar_chart = alt.Chart(df_melted).mark_bar().encode(
        y=alt.X('TEAMS:N', title='Teams'),
        x=alt.Y('Amount:Q', stack='zero', title='Amount'),
        color=alt.Color('Date:N', title='Date'),
        tooltip=['TEAMS:N', 'Date:N', 'Amount:Q'],
    ).properties(
        title="Stacked Bar Chart of Teams' Daily Contributions",
        height=400,
        width=800
    ).interactive()

    st.altair_chart(stacked_bar_chart, use_container_width=True)

# Panel for revenue trend line and area charts
with st.expander("Revenue Trend Charts", expanded=True):
    columns = st.columns([1, 1])

    with columns[0]:
        # Line chart for revenue collected trend
        line_chart = alt.Chart(df_melted).mark_line().encode(
            x=alt.X('Date:N', title='DATE'),
            y=alt.Y('Amount:Q', stack='zero', title='Amount'),
            color=alt.Color('TEAMS:N', title='TEAMS'),
            tooltip=['TEAMS:N', 'Date:N', 'Amount:Q']
        ).properties(
            title="Revenue Collected Trend",
            width=600
        ).interactive()

        st.altair_chart(line_chart, use_container_width=True)

    with columns[1]:
        # Area chart for revenue collected area trend
        area_chart = alt.Chart(df_melted).mark_area().encode(
            x=alt.X('Date:N', title='DATE'),
            y=alt.Y('Amount:Q', stack='zero', title='Amount'),
            color=alt.Color('TEAMS:N', title='TEAMS'),
            tooltip=['TEAMS:N', 'Date:N', 'Amount:Q']
        ).properties(
            title="Revenue Collected Area Trend",
            height=400,
            width=600
        ).interactive()

        st.altair_chart(area_chart, use_container_width=True)

# Panel for pie and donut charts
with st.expander("Pie and Donut Charts", expanded=True):
    pie = st.columns([4, 1])

    with pie[0]:
        # Bar chart for team distribution ranking
        pie_chart = alt.Chart(team_totals).mark_bar().encode(
            alt.X('TOTAL:Q', axis=None),
            alt.Y('TEAMS:O', sort='-x'),
            color=alt.Color('TEAMS:N', legend=None)
        ).properties(
            title='Team Distribution Ranking'
        )
        st.altair_chart(pie_chart, use_container_width=True)

    with pie[1]:
        # Donut chart for revenue collected by teams
        donut_chart = alt.Chart(df).mark_arc(innerRadius=70).encode(
            theta=alt.Theta("TOTAL:Q"),
            color=alt.Color("TEAMS:N"),
            tooltip=['TEAMS:N', 'TOTAL:Q']
        ).properties(
            title="Revenue Collected By Teams",
            height=400,
            width=400
        )
        st.altair_chart(donut_chart, use_container_width=True)
