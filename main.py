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
# print(container)

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

##################################################################
print("\n")
##################################################################

container2 = soup.find_all("div", class_ = "bixbox")[2]
# print(container)

section = container2.find("div", class_ = "releases")
header2 = section.find("span")
# print(header2.text)
header2 = header2.text

boxes = container2.find_all("div", class_ = "tt")
# print(boxes)

titles2 = []
for i in boxes:
    title = i.text.strip('\n \t')
    titles2.append(title)
# print(titles2)

##################################################################

data = {header1: titles1, header2: titles2}

df = pd.DataFrame(data)
print(df)

df.to_csv("animasu-update-anime.csv", index = False)

df = pd.read_csv("animasu-update-anime.csv")

st.title("Update Anime Hari ini di animasu.cc")
st.divider()
st.write(df)

if st.button("Refresh", type="primary"):
    st.rerun()



