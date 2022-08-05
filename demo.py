import requests
import streamlit as st

st.set_page_config(page_title="Rich Text Segmentation Demo")


@st.experimental_memo(ttl=600)
def get_results(URL):
    response = requests.get(URL).json()

    if response["meta"]["errors"]:
        st.error("Could not fetch results for the selected search parameters.")
        st.code(response, language="json")
        st.stop()

    return response["response"]["results"]


st.header("Rich Text Segmentation Test")

st.sidebar.write("# Configuration")
st.sidebar.write("### Search Parameters")
EXPERIENCE_KEY = st.sidebar.text_input("Experience Key", value="yext_help_site")
API_KEY = st.sidebar.text_input("API Key", value="1c81e4de0ec0e8051bdf66c31fc26a45")
VERTICAL_KEY = st.sidebar.text_input("Vertical Key", value="help_articles")
FIELD = st.sidebar.text_input("Field", value="body")


URL = f"https://liveapi.yext.com/v2/accounts/me/search/vertical/query?experienceKey={EXPERIENCE_KEY}&api_key={API_KEY}&limit=50&v=20220101&version=STAGING&locale=en&verticalKey={VERTICAL_KEY}&input="
results = get_results(URL)
fields = []
offset = 50
while results:
    fields += [r["data"][FIELD] for r in results]

    NEW_URL = URL + f"&offset={offset}"
    offset += 50
    results = get_results(NEW_URL)

selection = st.selectbox(label="", options=fields)
print(selection)
segments = selection.split("\n")
segments = [segment.strip() for segment in segments]
segments = [segment for segment in segments if segment]
print(segments)

left, right = st.columns(2)
left.write("### Original Rich Text")
right.write("### Segmented Rich Text")
left.markdown(selection)
for segment in segments:
    right.info(segment)


right.write()
