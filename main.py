import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://v9.animasu.cc/"
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

try:
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()  # This will raise an exception for bad status codes

    soup = BeautifulSoup(r.text, "lxml")
    container1 = soup.find_all("div", class_="bixbox")

    if not container1 or len(container1) < 2:
        st.error("Unable to fetch data. The website structure might have changed or the request was blocked.")
        st.stop()

    container1 = container1[1]
    section = container1.find("div", class_="releases")

    header1 = section.find("span")
    header1 = header1.text

    boxes = container1.find_all("div", class_="tt") or []
    titles1 = [i.text.strip('\n \t') for i in boxes]

    episodes = container1.find_all("span", class_="epx") or []
    episodes_1 = [i.text for i in episodes]

    # Second container
    container2 = soup.find_all("div", class_="bixbox")

    if not container2 or len(container2) < 2:
        st.error("Unable to fetch data. The website structure might have changed or the request was blocked.")
        st.stop()

    container2_data = container2[2]
    section = container2_data.find("div", class_="releases")
    header2 = section.find("span")
    header2 = (header2.text if header2 else "Completed Series") + " (Completed)"

    boxes = container2_data.find_all("div", class_="tt") or []
    titles2 = [i.text.strip('\n \t') for i in boxes]

    episodes = container2_data.find_all("span", class_="epx") or []
    episodes_2 = [i.text for i in episodes]

except requests.RequestException as e:
    st.error(f"Error fetching data: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.stop()

# Create DataFrame
data = {
    header1: titles1,
    "Eps": episodes_1,
    header2: titles2,
    "Eps Total": episodes_2
}

# Ensure all lists have the same length
max_len = max(len(titles1), len(episodes_1), len(titles2), len(episodes_2))
data[header1] = titles1 + [''] * (max_len - len(titles1))
data["Eps"] = episodes_1 + [''] * (max_len - len(episodes_1))
data[header2] = titles2 + [''] * (max_len - len(titles2))
data["Eps Total"] = episodes_2 + [''] * (max_len - len(episodes_2))

df = pd.DataFrame(data)

# Streamlit UI
st.set_page_config(
        page_title="Animasu Anime Updates",
        page_icon="🎬",
    )

st.header("Update Anime Hari ini di animasu.cc")
st.subheader("By Ahmad Fauzan")
st.divider()

st.write(df)

left, right = st.columns(2)

if left.button("Refresh", type="secondary", use_container_width=True):
    st.rerun()
right.link_button("Link Animasu", url="https://v9.animasu.cc/", use_container_width=False, type="tertiary")