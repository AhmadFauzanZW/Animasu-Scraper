import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import time
import logging
from typing import List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
URL = "https://v9.animasu.cc/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def fetch_webpage(url: str, headers: dict) -> Optional[BeautifulSoup]:
    """
    Fetch webpage content with error handling.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        logger.error(f"Request failed: {str(e)}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")
        return None


def extract_anime_data(container) -> Tuple[str, List[str], List[str]]:
    """
    Extract anime titles and episodes from a container.
    """
    try:
        section = container.find("div", class_="releases")
        header = section.find("span").text

        boxes = container.find_all("div", class_="tt")
        titles = [box.text.strip('\n \t') for box in boxes]

        episodes = container.find_all("span", class_="epx")
        episode_list = [ep.text for ep in episodes]

        return header, titles, episode_list
    except AttributeError as e:
        logger.error(f"Error extracting data: {str(e)}")
        raise Exception("Failed to extract anime data: website structure might have changed")


def create_dataframe(data1: tuple, data2: tuple) -> pd.DataFrame:
    """
    Create a DataFrame from the extracted data.
    """
    header1, titles1, episodes_1 = data1
    header2, titles2, episodes_2 = data2

    data = {
        header1: titles1,
        "Eps": episodes_1,
        f"{header2} (Completed)": titles2,
        "Eps Total": episodes_2
    }

    return pd.DataFrame(data)


def main():
    st.set_page_config(
        page_title="Animasu Anime Updates",
        page_icon="🎬",
        layout="wide"
    )

    st.header("Update Anime Hari ini di animasu.cc")
    st.subheader("By Ahmad Fauzan")
    st.divider()

    # Add a retry mechanism for failed requests
    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            soup = fetch_webpage(URL, HEADERS)
            if soup is None:
                raise Exception("Failed to fetch webpage")

            containers = soup.find_all("div", class_="bixbox")
            if len(containers) < 3:
                raise Exception("Website structure has changed: not enough containers found")

            # Extract data from containers
            data1 = extract_anime_data(containers[1])
            data2 = extract_anime_data(containers[2])

            # Create and display DataFrame
            df = create_dataframe(data1, data2)

            # Save to CSV
            try:
                df.to_csv("animasu-update-anime.csv", index=False)
            except Exception as e:
                st.warning(f"Could not save to CSV: {str(e)}")
                logger.warning(f"CSV save failed: {str(e)}")

            # Display the DataFrame
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # Create columns for buttons
            left, right = st.columns(2)

            if left.button("Refresh", type="secondary", use_container_width=True):
                st.rerun()

            right.link_button(
                "Link Animasu",
                url=URL,
                use_container_width=False,
                type="tertiary"
            )

            break  # Success, exit retry loop

        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(retry_delay)
            else:
                st.error("Failed to fetch anime updates. Please try again later.")
                logger.error(f"All retry attempts failed: {str(e)}")


if __name__ == "__main__":
    main()