import streamlit as st
import altair as alt
import pandas as pd

# Load the data from excel. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_excel("data/logbook.xlsx")
    return df


df = load_data()


st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

''

st.table(df)
