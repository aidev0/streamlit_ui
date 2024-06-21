import os
import requests
import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
MONGO_DB_URL = os.environ.get('MONGO_DB_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_DB_URL)
database_name = os.environ.get('DATABASE_NAME', 'vida_ai')

db = client[database_name]
leads_collection = db.leads
campaigns_collection = db.campaigns

st.set_page_config(
    page_title="Praisidio Email Campaign Leads",
    layout="wide"
)


def fetch_data(campaign_id):
    campaign_leads_url = f"https://salty-cove-64673-5fe07b0600ae.herokuapp.com/api/data/leads_features/{campaign_id}"
    response = requests.get(campaign_leads_url)
    if response.status_code == 200:
        data = response.json()
    else:
        st.error(f"Failed to retrieve data. Status Code: {response.status_code}")
        data = [{'status': 'failed'}]
    return pd.DataFrame(data)


def get_renderer():
    if "campaign_id" in st.query_params:
        campaign_id = st.query_params["campaign_id"]
        df = fetch_data(campaign_id)
        campaign = campaigns_collection.find_one({'_id': ObjectId(campaign_id)})
        if campaign:
            st.title(campaign.get("description", "Campaign Leads"))
        else:
            st.title("Campaign Leads")
    else:
        df = pd.DataFrame([{'status': 'failed'}])
        st.title("No Campaign Selected")
    return StreamlitRenderer(df)


renderer = get_renderer()
renderer.explorer()
