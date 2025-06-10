# IMPORTANT: THE STREAMLIT APP WILL NOT RUN IN THIS ENVIRONMENT.
# NEED TO RUN IT SEPARATELY IN A STREAMLIT ENVIRONMENT.
# IT WAS ADDED AS PART OF THE NOTEBOOK FOR COMPLETENESS.
# IT IS PART OF THE NEXT STEP IN THE PROJECT.

import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry

# Must be the first Streamlit call
st.set_page_config(layout="wide")

# -----------------------------
# Load and preprocess your data
# -----------------------------

@st.cache_data
def load_data():
    # Replace this with your actual dataset path
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

# Required columns: country (alpha-2), fraud_label, alert, drn
# Add 3-letter country codes
def convert_country_alpha2_to_alpha3(alpha2):
    try:
        return pycountry.countries.get(alpha_2=alpha2).alpha_3
    except:
        return None

df["country_3"] = df["country"].apply(convert_country_alpha2_to_alpha3)
df = df.dropna(subset=["country_3"])  # Drop unknown countries

# -----------------------------
# Aggregate country-level stats
# -----------------------------

country_stats = df.groupby("country_3").agg(
    fraud_count=("fraud_label", "sum"),
    total_transactions=("drn", "count")
).reset_index()

country_stats["fraud_severity"] = (
    country_stats["fraud_count"] / country_stats["fraud_count"].max()
).fillna(0)

# -----------------------------
# Streamlit layout
# -----------------------------

st.title("Fraud Map and Country-Level Insights")

# Choropleth map using Plotly
fig = px.choropleth(
    country_stats,
    locations="country_3",
    color="fraud_severity",
    color_continuous_scale=["green", "yellow", "red"],
    hover_name="country_3",
    hover_data={
        "fraud_count": True,
        "total_transactions": True,
        "fraud_severity": False,
    },
)

fig.update_layout(
    title="Fraud Severity by Country",
    coloraxis_colorbar=dict(title="Fraud Severity"),
    margin=dict(l=0, r=0, t=50, b=0),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Country details on selection
# -----------------------------

selected_country = st.selectbox(
    "Select a country to view details:", country_stats["country_3"].sort_values()
)

country_info = country_stats[country_stats["country_3"] == selected_country].squeeze()

st.markdown(f"""
### Country: {selected_country}

- **Total Transactions:** {country_info['total_transactions']}
- **Fraud Cases:** {int(country_info['fraud_count'])}
""")
