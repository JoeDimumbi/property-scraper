import requests
from bs4 import BeautifulSoup
import csv
import os
import random
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='scraper_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# User-Agent list for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

# Error-handling request function
def fetch_url(url, retries=3, wait=2):
    for attempt in range(retries):
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            logging.warning(f"HTTP error {http_err} on attempt {attempt + 1} for URL: {url}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request failed: {req_err} on URL: {url}")
        time.sleep(wait * (attempt + 1))
    return None

# Scrape city IDs from Property24
def scrape_property24_city_ids():
    url = "https://www.property24.com/vacant-land-for-sale/all-cities/western-cape/9"
    response = fetch_url(url)
    city_ids = []
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        inputs = soup.find_all('input', {'name': 'AllCityIds'})
        for input_tag in inputs:
            value = input_tag.get('value', 'N/A')
            label = input_tag.find_parent('label')
            city_name = label.find('a').get_text(strip=True) if label else "N/A"
            if city_name != "N/A" and value != "N/A":
                city_ids.append({"City": city_name, "ID": value})
    else:
        logging.error("Failed to scrape Property24 city IDs.")
    return city_ids

# Generate Property24 URLs from city IDs
def generate_property24_urls(city_ids):
    urls = []
    for city in city_ids:
        city_name = city["City"].lower().replace(" ", "-")
        city_id = city["ID"]
        url = f"https://www.property24.com/vacant-land-for-sale/{city_name}/western-cape/{city_id}"
        urls.append(url)
    return urls

# Scrape listings from Property24
def scrape_property24_listings(urls, filename="property24_listings.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Price", "Location", "Address", "Erf Size", "Link", "Date Added"])
        if not file_exists:
            writer.writeheader()
        for url in urls:
            response = fetch_url(url)
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                listings = soup.find_all(class_="p24_content")
                for listing in listings:
                    writer.writerow({
                        "Price": listing.find(class_="p24_price").get_text(strip=True) if listing.find(class_="p24_price") else "N/A",
                        "Location": listing.find(class_="p24_location").get_text(strip=True) if listing.find(class_="p24_location") else "N/A",
                        "Address": listing.find(class_="p24_address").get_text(strip=True) if listing.find(class_="p24_address") else "N/A",
                        "Erf Size": listing.find(class_="p24_size").get_text(strip=True) if listing.find(class_="p24_size") else "N/A",
                        "Link": url,
                        "Date Added": datetime.now().strftime('%Y-%m-%d')
                    })
            else:
                logging.error(f"Failed to fetch listings from {url}")
            time.sleep(random.uniform(1, 3))

# Scrape listings from PrivateProperty
def scrape_privateproperty_listings(base_url, filename="privateproperty_listings.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Price", "Title", "Address", "Suburb", "Features", "Link", "Date Added"])
        if not file_exists:
            writer.writeheader()
        for page in range(1, 6):  # Example: scrape first 5 pages
            url = f"{base_url}?page={page}"
            response = fetch_url(url)
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                listings = soup.find_all(class_="listing-result")
                for listing in listings:
                    writer.writerow({
                        "Price": listing.find(class_="listing-result__price txt-heading-2").get_text(strip=True) if listing.find(class_="listing-result__price txt-heading-2") else "N/A",
                        "Title": listing.find(class_="listing-result__title txt-base-regular").get_text(strip=True) if listing.find(class_="listing-result__title txt-base-regular") else "N/A",
                        "Address": listing.find(class_="listing-result__address txt-base-regular").get_text(strip=True) if listing.find(class_="listing-result__address txt-base-regular") else "N/A",
                        "Suburb": listing.find(class_="listing-result__desktop-suburb").get_text(strip=True) if listing.find(class_="listing-result__desktop-suburb") else "N/A",
                        "Features": listing.find(class_="listing-result__features").get_text(strip=True) if listing.find(class_="listing-result__features") else "N/A",
                        "Link": url,
                        "Date Added": datetime.now().strftime('%Y-%m-%d')
                    })
            else:
                logging.error(f"Failed to fetch listings from {url}")
            time.sleep(random.uniform(1, 3))

# Main execution
def main():
    logging.info("Starting combined Property24 and PrivateProperty scraping process.")
    city_ids = scrape_property24_city_ids()
    if city_ids:
        p24_urls = generate_property24_urls(city_ids)
        scrape_property24_listings(p24_urls)
        scrape_privateproperty_listings("https://www.privateproperty.co.za/for-sale/western-cape")
        logging.info("Scraping completed successfully.")
    else:
        logging.error("No city IDs retrieved; scraping aborted.")

if __name__ == "__main__":
    main()
