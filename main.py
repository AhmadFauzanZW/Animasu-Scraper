import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://v9.animasu.cc/"
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

r = requests.get(url, headers=HEADERS)
print(r)

soup = BeautifulSoup(r.text, "lxml")

#First container
container1 = soup.find_all("div", class_="bixbox")

# Process first section
container1_data = container1[1]
section = container1_data.find("div", class_="releases")

header1 = section.find("span")
header1 = header1.text

boxes = container1_data.find_all("div", class_="tt") or []
titles1 = [i.text.strip('\n \t') for i in boxes]

episodes = container1_data.find_all("span", class_="epx") or []
episodes_1 = [i.text for i in episodes]

# Second container
container2 = soup.find_all("div", class_="bixbox")

container2_data = container2[2]
section = container2_data.find("div", class_="releases")
header2 = section.find("span")
header2 = (header2.text if header2 else "Completed Series") + " (Completed)"

boxes = container2_data.find_all("div", class_="tt") or []
titles2 = [i.text.strip('\n \t') for i in boxes]

episodes = container2_data.find_all("span", class_="epx") or []
episodes_2 = [i.text for i in episodes]

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
st.header("Update Anime Hari ini di animasu.cc")
st.subheader("By Ahmad Fauzan")
st.divider()

st.write(df)

left, right = st.columns(2)

if left.button("Refresh", type="secondary", use_container_width=True):
    st.rerun()
right.link_button("Link Animasu", url="https://v9.animasu.cc/", use_container_width=False, type="tertiary")