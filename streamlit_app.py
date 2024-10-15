import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 


# Load the data from excel. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_excel("data/logbook.xlsx")
    df[['style','style category']] = df['Style'].str.split(' ',expand=True)
    df=df.drop(columns=['Style'])
    df.rename(columns={'Partner(s)': 'Partner'}, inplace=True)
    #add index
    df['log_id'] = df.index + 1
    #convert date
    df['Date']=pd.to_datetime(df['Date'], format='%d/%b/%y')
    df["first star"]= df["Grade"].str.find('*')
    df[['overall grade','technical grade', 'star rating']] = df['Grade'].str.split(' ',expand=True)
    return df


df = load_data()

# we want to count logs by partner

    # Split the 'Partner' column by the delimiter ','
    df_split = df.assign(Partner=df['Partner'].str.split(','))
    
    # Explode the 'Partner' column to create a new row for each partner
    df_split = df_split.explode('Partner')
    
    # Strip any leading/trailing whitespace from the 'Partner' column
    df_split['Partner'] = df_split['Partner'].str.strip()
    
    # Reorder the columns for clarity
    df_split = df_split[['log_id', 'Grade Type', 'Partner']]
    
    #creating counts of logs by partner
    
    partner=df_split.groupby(['Partner']).size().reset_index(name='counts')
    partner=partner.sort_values('counts', ascending=False)
    
    #counts of logs by route type
    route_type=df_split.groupby(['Grade Type']).size().reset_index(name='counts')
    
    ##creating counts of logs by partner by grade type
    
    partner_type=df_split.groupby(['Grade Type','Partner']).size().reset_index(name='counts')
    
    #sort
    route_type=route_type.sort_values('counts', ascending=False)
    partner_type=partner_type.sort_values('counts', ascending=False)
    partner=partner.sort_values('counts', ascending=False)

fig=px.bar(partner,x='counts',y='Partner', orientation='h')
st.write(fig)

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

''

st.table(df)
