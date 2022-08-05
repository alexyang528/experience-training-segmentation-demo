import requests
import streamlit as st

st.set_page_config(page_title="Rich Text Segmentation Demo", layout="wide")


@st.experimental_memo(ttl=600)
def get_results(URL):
    return requests.get(URL).json()


st.header("Rich Text Segmentation Test")

st.sidebar.write("# Configuration")
st.sidebar.write("### Search Parameters")
EXPERIENCE_KEY = st.sidebar.text_input("Experience Key", value="yext_help_site")
API_KEY = st.sidebar.text_input("API Key", value="1c81e4de0ec0e8051bdf66c31fc26a45")
VERTICAL_KEY = st.sidebar.text_input("Vertical Key", value="help_articles")
FIELD = st.sidebar.text_input("Field", value="body")


URL = f"https://liveapi.yext.com/v2/accounts/me/search/vertical/query?experienceKey={EXPERIENCE_KEY}&api_key={API_KEY}&limit=50&v=20220101&version=STAGING&locale=en&verticalKey={VERTICAL_KEY}&input="
response = get_results(URL)
if response["meta"]["errors"]:
    st.error("Could not fetch results for the selected search parameters.")
    st.json(response)
    st.stop()
results = response["response"]["results"]
fields = []
offset = 50
while results:
    try:
        fields += [r["data"][FIELD] for r in results]
    except:
        st.error("Could not fetch field from results.")
        st.json(response)
        st.stop

    NEW_URL = URL + f"&offset={offset}"
    offset += 50
    response = get_results(NEW_URL)
    if response["meta"]["errors"]:
        st.error("Could not fetch results for the selected search parameters.")
        st.json(response)
        st.stop()
    results = response["response"]["results"]

selection = st.selectbox(label="", options=fields)
segments = selection.split("\n")
segments = [segment.strip() for segment in segments]
segments = [segment for segment in segments if segment]

left, right = st.columns(2)
left.write("### Original Rich Text")
right.write("### Segmented Rich Text")
left.markdown(selection)
for segment in segments:
    right.info(segment)
