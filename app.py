import streamlit as st
import pandas as pd
import os

# ------------------------------
# CONFIGURATION
# ------------------------------
DATA_FILE = "data.csv"  # CSV with SOURCEURL, DATEADDED, ImportanceScore_2, country, Summary
NOT_RELEVANT_FILE = "not_relevant_urls.csv"

@st.cache_data
def load_data():
    """Load and preprocess the dataset."""
    if not os.path.exists(DATA_FILE):
        st.error(f"Data file {DATA_FILE} not found!")
        return pd.DataFrame(columns=['SOURCEURL', 'DATEADDED', 'ImportanceScore_2', 'country', 'Summary'])

    df = pd.read_csv(DATA_FILE, sep=None, engine='python')
    required_cols = ['SOURCEURL', 'DATEADDED', 'ImportanceScore_2', 'country', 'Summary']
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing column '{col}' in data.csv. Please fix the CSV header.")
            st.stop()

    df['DATEADDED'] = pd.to_datetime(df['DATEADDED'], format='%Y%m%d', errors='coerce').dt.date
    return df

def save_not_relevant(url, summary):
    if not os.path.exists(NOT_RELEVANT_FILE):
        pd.DataFrame(columns=['URL', 'Summary']).to_csv(NOT_RELEVANT_FILE, index=False)
    existing = pd.read_csv(NOT_RELEVANT_FILE)
    if url not in existing['URL'].values:
        new_row = pd.DataFrame([[url, summary]], columns=['URL', 'Summary'])
        updated = pd.concat([existing, new_row], ignore_index=True)
        updated.to_csv(NOT_RELEVANT_FILE, index=False)

st.title("News URL Review Dashboard")
data = load_data()

st.sidebar.header("Filters")

country_options = sorted([c for c in data['country'].dropna().unique() if str(c).strip() != ''])
selected_countries = st.sidebar.multiselect("Select Country", country_options)
date_options = sorted(data['DATEADDED'].dropna().unique())
selected_dates = st.sidebar.multiselect("Select Date", date_options)

filtered_data = data.copy()
if selected_countries:
    filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
if selected_dates:
    filtered_data = filtered_data[filtered_data['DATEADDED'].isin(selected_dates)]

st.write("### Filtered URLs")
if filtered_data.empty:
    st.info("No data matches your filters.")
else:
    for idx, row in filtered_data.iterrows():
        with st.container():
            cols = st.columns([3, 5, 2])
            with cols[0]:
                st.markdown(f"[{row['SOURCEURL']}]({row['SOURCEURL']})")
            with cols[1]:
                st.write(row['Summary'])
            with cols[2]:
                if st.checkbox("Not Relevant", key=f"chk_{idx}"):
                    save_not_relevant(row['SOURCEURL'], row['Summary'])

st.write("---")
st.write(f"**Not Relevant URLs are saved in:** `{NOT_RELEVANT_FILE}`")
