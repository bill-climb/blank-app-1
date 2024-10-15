import streamlit as st
st.set_page_config(layout="wide")
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
route_type=route_type.sort_values('counts', ascending=True)
partner_type=partner_type.sort_values('counts', ascending=True)
partner=partner.sort_values('counts', ascending=True)

# Find the partner with the most counts
max_counts_row = partner.loc[partner['counts'].idxmax()]
most_counts_partner = max_counts_row['Partner']
most_counts_value = max_counts_row['counts']

# Generate summary text
summary_text = f"You climbed the most with {most_counts_partner} - {most_counts_value} logs!"

# Generate humorous text based on the number of partners
num_partners = len(partner)

if num_partners < 5:
    funny_text = f"You only climbed with {num_partners} people this year. Looks like a small gathering! Do you need some more friends?!"
elif num_partners < 10:
    funny_text = f"You climbed with {num_partners} people this year. Enough for a fun game night i suppose!"
else:
    funny_text = f"You climbed with {num_partners} people this year. Wow, we've got a whole crowd! It's like a party in here!"

# Combine the summary and humorous text
partner_text = summary_text + " " + funny_text


#content
st.title("🎈 UKC Log Dashboard")
st.write(
    "Analyse your logs"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.write(partner_text)
    partner_fig=px.bar(partner,x='counts',y='Partner', orientation='h')
    st.write(partner_fig)

with col2:
    st.write("Types of climbing")   
    import plotly.graph_objects as go
    labels = route_type['Grade Type']
    values = route_type['counts']
    route.fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                 insidetextorientation='radial'
                                )])
    st.write(route_fig)

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

''

''





st.table(df)
