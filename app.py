import streamlit as st
import pandas as pd
import os

# ------------------------------
# CONFIGURATION
# ------------------------------
DATA_FILE = "data.csv"  # The CSV file with columns: Country, Date, URL, Summary
NOT_RELEVANT_FILE = "not_relevant_urls.csv"

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------
@st.cache_data
def load_data():
    """Load the main dataset."""
    if not os.path.exists(DATA_FILE):
        st.error(f"Data file {DATA_FILE} not found!")
        return pd.DataFrame(columns=['country', 'DATADDED', 'SOURCEURL', 'Summary'])
    return pd.read_csv(DATA_FILE)

def save_not_relevant(url, summary):
    """Save the 'Not Relevant' URLs to a separate CSV file."""
    if not os.path.exists(NOT_RELEVANT_FILE):
        pd.DataFrame(columns=['URL', 'Summary']).to_csv(NOT_RELEVANT_FILE, index=False)
    existing = pd.read_csv(NOT_RELEVANT_FILE)
    if url not in existing['URL'].values:
        new_row = pd.DataFrame([[url, summary]], columns=['URL', 'Summary'])
        updated = pd.concat([existing, new_row], ignore_index=True)
        updated.to_csv(NOT_RELEVANT_FILE, index=False)

# ------------------------------
# MAIN APP
# ------------------------------
st.title("News URL Review Dashboard")

data = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect("Select Country", sorted(data['Country'].dropna().unique()))
selected_dates = st.sidebar.multiselect("Select Date", sorted(data['Date'].dropna().unique()))

# Apply filters
filtered_data = data.copy()
if selected_countries:
    filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
if selected_dates:
    filtered_data = filtered_data[filtered_data['DATEADDED'].isin(selected_dates)]

# Show results
st.write("### Filtered URLs")
if filtered_data.empty:
    st.info("No data matches your filters.")
else:
    for idx, row in filtered_data.iterrows():
        with st.container():
            cols = st.columns([3, 5, 2])  # URL, Summary, Checkbox
            with cols[0]:
                st.markdown(f"[{row['SOURCEURL']}]({row['SOURCEURL']})")
            with cols[1]:
                st.write(row['Summary'])
            with cols[2]:
                if st.checkbox("Not Relevant", key=f"chk_{idx}"):
                    save_not_relevant(row['URL'], row['Summary'])

st.write("---")
st.write(f"**Not Relevant URLs are saved in:** `{NOT_RELEVANT_FILE}`")
