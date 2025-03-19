import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Wikipedia URL containing the list of WWI battles
wiki_url = "https://en.wikipedia.org/wiki/List_of_World_War_I_battles"

# Headers to mimic a browser visit (avoid being blocked)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Fetch the main battles list page
response = requests.get(wiki_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all battle links (Wikipedia uses tables or lists for battles)
battle_links = []
for link in soup.find_all('a', href=True):
    if "Battle_of" in link['href'] and "/wiki/" in link['href']:
        full_link = "https://en.wikipedia.org" + link['href']
        battle_links.append(full_link)

# Remove duplicates
battle_links = list(set(battle_links))

# Prepare list to store battle data
battle_data = []

# Loop through battle pages and extract information
for battle_url in battle_links[:]:  # Limiting to 20 battles for now to test
    try:
        battle_response = requests.get(battle_url, headers=headers)
        battle_soup = BeautifulSoup(battle_response.text, 'html.parser')

        # Extract battle name (title of the page)
        battle_name = battle_soup.find("h1", {"id": "firstHeading"}).text.strip()

        # Extract Infobox (structured data in Wikipedia pages)
        infobox = battle_soup.find("table", {"class": "infobox"})
        battle_info = {"BattleName": battle_name, "URL": battle_url}

        if infobox:
            rows = infobox.find_all("tr")

            for row in rows:
                header = row.find("th")
                value = row.find("td")

                if header and value:
                    key = header.text.strip()
                    val = value.text.strip().replace("\n", " ")  # Remove line breaks

                    # Extract Date, Location, and Result
                    if "Date" in key:
                        battle_info["StartDate"] = val.split("–")[0].strip()
                        battle_info["EndDate"] = val.split("–")[1].strip() if "–" in val else battle_info["StartDate"]

                    elif "Location" in key:
                        battle_info["Location"] = val

                    elif "Result" in key or "Outcome" in key:
                        battle_info["Outcome"] = val

            # Extract Belligerents, Strength, and Casualties/Losses
            for section in ["Belligerents", "Strength", "Casualties and losses"]:
                section_element = infobox.find("th", string=section)
                if section_element:
                    row = section_element.find_next("tr")
                    if row:
                        columns = row.find_all("td", recursive=False)
                        if len(columns) == 2:
                            battle_info[f"{section}_Right"] = columns[0].text.strip()
                            battle_info[f"{section}_Left"] = columns[1].text.strip()

        # Append to the dataset
        battle_data.append(battle_info)
        time.sleep(1)  # Sleep to avoid being blocked

    except Exception as e:
        print(f"Error processing {battle_url}: {e}")

# Convert to DataFrame
wwi_battles_df = pd.DataFrame(battle_data)

# Save to CSV
csv_filename = "WW1_Battles_Detailed.csv"
wwi_battles_df.to_csv(csv_filename, index=False)

# Display dataset preview
print("Scraped WWI Battles Dataset (Detailed):")
print(wwi_battles_df.head())

# Confirm file saved
print(f"Dataset saved as: {csv_filename}")
