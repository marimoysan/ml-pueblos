import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Wikipedia base URL
BASE_URL = "https://es.wikipedia.org"
MAIN_URL = "https://es.wikipedia.org/wiki/Anexo:Municipios_de_Espa%C3%B1a"


def get_province_links():
    """Scrapes Wikipedia to get all province municipality list links."""
    response = requests.get(MAIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    province_links = {}
    
    # Use the provided CSS selector to extract province links
    for link in soup.select(".mw-content-ltr li > a"):
        href = link["href"]
        province_name = link.text.strip()

        # Ensure it's a valid province link
        if "Anexo:Municipios_de_" in href:
            province_links[province_name] = BASE_URL + href

    print(f"✅ Found {len(province_links)} provinces!")
    return province_links


def get_municipality_links(province_url):
    """Scrapes a province's Wikipedia page to get all municipality links."""
    response = requests.get(province_url)
    soup = BeautifulSoup(response.text, "html.parser")

    municipality_links = {}

    # Look for all municipality links inside tables
    tables = soup.find_all("table", class_="wikitable")

    for table in tables:
        for row in table.find_all("tr")[1:]:  # Skip the header row
            cells = row.find_all("td")
            if cells:
                link = cells[0].find("a")
                if link:
                    town_name = link.text.strip()
                    municipality_links[town_name] = BASE_URL + link["href"]

    print(f"  ✅ Found {len(municipality_links)} municipalities in province.")
    return municipality_links


def scrape_municipality_data(municipality_url):
    """Extracts details from a municipality's Wikipedia page, including INE code and a valid image."""
    response = requests.get(municipality_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract municipality name
    title = soup.find("h1").text.strip()

    # Extract data from the infobox
    infobox = soup.find("table", class_="infobox")
    data = {"Municipio": title, "Wikipedia URL": municipality_url}

    if infobox:
        for row in infobox.find_all("tr"):
            cells = row.find_all(["th", "td"])
            if len(cells) == 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                data[key] = value

    # 🔹 Find the first valid image (NOT "Escudo" or "Bandera")
    valid_image_url = "No image available"
    if infobox:
        for img in infobox.find_all("img"):
            img_src = "https:" + img["src"]
            img_filename = img_src.split("/")[-1].lower()

            # 🔥 Exclude images containing "escudo" or "bandera"
            if "escudo" not in img_filename and "bandera" not in img_filename:
                valid_image_url = img_src
                break  # Stop at the first valid image

    data["Image URL"] = valid_image_url

    # Extract first paragraph (summary)
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        if len(p.text.strip()) > 100:  # Avoid very short text
            data["Description"] = p.text.strip()
            break

    # 🔹 Extract INE Code dynamically
    ine_code = None
    for li in soup.find_all("li"):
        link = li.select_one(".uid a")  # Find any <a> inside .uid
        if link and "INE" in li.text:
            ine_code = link.text.strip()
            break  # Stop after finding the first match

    data["INE Code"] = ine_code if ine_code else "Not available"

    return data






def scrape_all_municipalities():
    """Scrapes all municipalities and saves data incrementally after every 10 entries."""
    province_links = get_province_links()

    if not province_links:
        print("❌ No province links found. Exiting.")
        return

    all_municipalities = []
    counter = 0  # Track how many municipalities have been scraped

    for province, province_url in province_links.items():
        print(f"📍 Scraping province: {province}...")
        municipality_links = get_municipality_links(province_url)

        if not municipality_links:
            print(f"⚠️ No municipalities found for {province}. Skipping...")
            continue

        for town, town_url in municipality_links.items():
            print(f"  - Scraping town: {town}...")
            town_data = scrape_municipality_data(town_url)
            town_data["Province"] = province  # Add province data
            all_municipalities.append(town_data)
            counter += 1  # Increment counter

            # 🔹 Save progress every 10 towns
            if counter % 10 == 0:
                df = pd.DataFrame(all_municipalities)
                df.to_csv("spanish_municipalities.csv", index=False, encoding="utf-8")
                print(f"💾 Saved progress after {counter} municipalities.")

            # Sleep to avoid getting blocked
            time.sleep(1)

    # 🔹 Final save at the end
    if all_municipalities:
        df = pd.DataFrame(all_municipalities)
        df.to_csv("spanish_municipalities.csv", index=False, encoding="utf-8")
        print("✅ Final data saved to spanish_municipalities.csv")


    # Save data to CSV
    df = pd.DataFrame(all_municipalities)
    df.to_csv("spanish_municipalities.csv", index=False, encoding="utf-8")
    print("✅ Data saved to spanish_municipalities.csv")


# Run the scraper
scrape_all_municipalities()
