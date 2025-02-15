import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

url = "https://v9.animasu.cc/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# r = response
r = requests.get(url, headers=HEADERS)
# print(r)

soup = BeautifulSoup(r.text, "lxml")
# print(soup)

container1 = soup.find_all("div", class_ = "bixbox")[1]
# print(container1)

section = container1.find("div", class_ = "releases")
header1 = section.find("span")
# print(header1.text)
header1 = header1.text

boxes = container1.find_all("div", class_ = "tt")
# print(boxes)

titles1 = []
for i in boxes:
    title = i.text.strip('\n \t')
    titles1.append(title)
# print(titles1)

episodes = container1.find_all("span", class_ = "epx")
# print(episodes)

episodes_1 = []
for i in episodes:
    episode = i.text
    episodes_1.append(episode)
# print(episodes_1)

##################################################################
print("\n")
##################################################################

container2 = soup.find_all("div", class_ = "bixbox")[2]
# print(container)

section = container2.find("div", class_ = "releases")
header2 = section.find("span")
# print(header2.text)
header2 = header2.text + " (Completed)"

boxes = container2.find_all("div", class_ = "tt")
# print(boxes)

titles2 = []
for i in boxes:
    title = i.text.strip('\n \t')
    titles2.append(title)
# print(titles2)

episodes = container2.find_all("span", class_ = "epx")
# print(episodes)

episodes_2 = []
for i in episodes:
    episode = i.text
    episodes_2.append(episode)
# print(episodes_2)

##################################################################

data = {header1: titles1, "Eps": episodes_1, header2: titles2, "Eps Total": episodes_2}

df = pd.DataFrame(data)
print(df)

df.to_csv("animasu-update-anime.csv", index = False)

df = pd.read_csv("animasu-update-anime.csv")

st.header("Update Anime Hari ini di animasu.cc")
st.subheader("By Ahmad Fauzan")
st.divider()
st.write(df)

left, right = st.columns(2)

if left.button("Refresh", type="secondary", use_container_width=True):
    st.rerun()
right.link_button("Link Animasu", url="https://v9.animasu.cc/", use_container_width=False, type="tertiary")



