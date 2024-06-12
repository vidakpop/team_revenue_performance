import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import base64
#page setup
st.set_page_config(
    layout='wide'
)
#loading the dataset
df=pd.read_csv('revenue_3(1).csv')

teams=['All Teams']+ list(df['TEAMS'].unique())

#st.header('COUNTY GOVERNMENT OF UASIN GISHU')
#add logo
# Function to load an image and convert it to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# URL or path to your logo
logo_path = "logo.png"  

# Get the base64 encoded image
logo_base64 = get_image_base64(logo_path)

# Using HTML and CSS to center the image
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

st.markdown("<div style='background:'black''><h1 style='color:#ac2217;display:flex;justify-content: center'>DIRECTORATE OF LICENSING AND COMPLIANCE</h1></div>",unsafe_allow_html=True)
st.title('Team Performance Revenue Analysis')
#st.dataframe(df)
#interface

st.sidebar.title('Revenue Team Analysis')

teams_panel=st.container()
with teams_panel:
    team=st.selectbox('Select Team',options=teams)
    if team=='All Teams':
        st.dataframe(df)
    else:
        team_df=df[df['TEAMS']==team]
        st.dataframe(team_df)

chart1,chart2=st.columns([1,2])

with chart1:
    # Create a pie chart
    team_totals = df.groupby('TEAMS')['TOTAL'].sum().reset_index()
    pie_chart = alt.Chart(team_totals).mark_bar().encode(
    alt.X('TOTAL:Q', axis=None),
    alt.Y('TEAMS:O', sort='-x'),
    color=alt.Color('TEAMS:N', legend=None)
    ).properties(
    #width=400,
    #height=400,
    title='Team Distribution Ranking'
    )
    st.altair_chart(pie_chart,use_container_width=True)


with chart2:
    #scatter plot
    c=alt.Chart(df).mark_bar().encode(
    x='TEAMS',
    y='TOTAL',
    color='TEAMS',
    tooltip=['27/05/2024','28/05/2024','29/05/2024','30/05/2024','31/05/2024'],
    
    ).properties(title="cumulative revenue trend by teams",
            #width=600
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
    chart2=c + text
    st.altair_chart(chart2,use_container_width=True)

cum_panel=st.container()
with cum_panel:
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

    st.altair_chart(stacked_bar_chart,use_container_width=True)

trend_panel=st.container()
with trend_panel:
    columns=st.columns([1,1])
    with columns[0]:
        # Melt the DataFrame to long format for daily data
        df_melted = df.melt(id_vars=["TEAMS", "TOTAL"], var_name="Date", value_name="Amount")

# line chart
        line_chart = alt.Chart(df_melted).mark_line().encode(
         x=alt.X('Date:N', title='DATE'),
        y=alt.Y('Amount:Q', stack='zero', title='Amount'),
        color=alt.Color('TEAMS:N', title='TEAMS'),
        tooltip=['TEAMS:N', 'Date:N', 'Amount:Q']
        ).properties(
         title="Revenue Collected Trend",
        #height=400,
        width=600
        ).interactive()

        st.altair_chart(line_chart,use_container_width=True)

    with columns[1]:
        # Melt the DataFrame to long format for daily data
        df_melted = df.melt(id_vars=["TEAMS", "TOTAL"], var_name="Date", value_name="Amount")

# area chart
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
        st.altair_chart(area_chart,use_container_width=True) #stacked_bar_chart


lastpanel=st.container()
with lastpanel:
    pie=st.columns([4,1])

    with pie[0]:
        # Create a pie chart
        team_totals = df.groupby('TEAMS')['TOTAL'].sum().reset_index()
        pie_chart = alt.Chart(team_totals).mark_bar().encode(
        alt.X('TOTAL:Q', axis=None),
        alt.Y('TEAMS:O', sort='-x'),
        color=alt.Color('TEAMS:N', legend=None)
         ).properties(
    #width=400,
    #height=400,
        title='Team Distribution Ranking'
         )
        st.altair_chart(pie_chart,use_container_width=True)

#arc=st.container()
        
    with pie[1]:
        donut_chart=alt.Chart(df).mark_arc(innerRadius=70).encode(
        theta=alt.Theta("TOTAL:Q"),
        color=alt.Color("TEAMS:N"),
        tooltip=['TEAMS:N', 'TOTAL:Q']
        ).properties(
        title="Revenue Collected By Teams",
        height=400,
         width=400
             )
        st.altair_chart(donut_chart,use_container_width=True)

