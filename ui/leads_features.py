import os

from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd
import streamlit as st
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv()

# Connect to MongoDB (update 'localhost' and '27017' with your MongoDB URI and port if needed)
MONGO_DB_URL = os.environ.get('MONGO_DB_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_DB_URL)
database_name = os.environ.get('DATABASE_NAME', 'vida_ai')
db = client[database_name]  # Replace 'your_database_name' with the name of your database
leads_collection = db.leads  # Assuming the MongoDB collection is named 'leads'


st.set_page_config(
    page_title="Praisidio Email Campaign Leads",
    layout="wide"
)

init_streamlit_comm()
st.title("Praisidio Email Campaign Leads")


@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
    st.text(st.query_params["campaign_id"])
    if "campaign_id" in st.query_params:
        leads = leads_collection.find({'campaign_id': st.query_params["campaign_id"]})
        df = pd.DataFrame(leads)
    else:
        df = pd.DataFrame([{'x': 0}])
        # df = pd.read_json("results/all_features_2024-06-11 21:51:45.121445.json")
    return StreamlitRenderer(df)


renderer = get_pyg_renderer()
renderer.explorer()