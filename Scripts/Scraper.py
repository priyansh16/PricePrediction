import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
from functools import wraps
import math


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class HemnetScraper:
    BASE_URL = 'https://www.hemnet.se/salda/bostader'
    CHROME_DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'  # update if needed
    MAX_PAGES = 10
    RETRY_LIMIT = 3

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--lang=en-US")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.data = {
            "Fritidshus": [],
            "Lägenhet": [],
            "Villa": [],
            "Kedjehus": [],
            "Parhus": [],
            "Tomt": []
        }

    def retry(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for attempt in range(1, self.RETRY_LIMIT + 1):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    logging.warning(f"Attempt {attempt} failed for {func.__name__}: {e}")
                    if attempt == self.RETRY_LIMIT:
                        logging.error(f"Exceeded max retries for {func.__name__}")
                        raise
                    time.sleep(2)
        return wrapper

    def get_all_page_urls(self):
        return [self.BASE_URL] + [f"{self.BASE_URL}?page={i}" for i in range(2, self.MAX_PAGES + 1)]
    
    @retry
    def get_listing_links(self, page_url):
        logging.info(f"Loading page {page_url}")
        self.driver.get(page_url)
        # self.handle_cookie_popup()
        self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Container_cardWrapper__ZE0kA")))
        cards = self.driver.find_elements(By.CLASS_NAME, "Container_cardWrapper__ZE0kA")

        links = []
        for card in cards:
            anchors = card.find_elements(By.TAG_NAME, "a")
            for a in anchors:
                href = a.get_attribute("href")
                if href:
                    links.append(href)

        # sometimes the first two links might not be listings, mimic previous behavior of skipping first two
        return links[2:] if len(links) > 2 else links

    @retry
    def extract_listing_data(self, listing_url):
        logging.info(f"Extracting data from {listing_url}")
        self.driver.get(listing_url)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Heading_hclHeading__KufPZ")))

        data = []
        name = self.driver.find_element(By.CLASS_NAME, "Heading_hclHeading__KufPZ").text
        data.append(name)
        
        # Locate the div containing final price by its class
        price_div = self.driver.find_element(By.CLASS_NAME, "SaleAttributes_sellingPrice__iFujI")

        # Extract both spans inside it (label and amount)
        spans = price_div.find_elements(By.CLASS_NAME, "SaleAttributes_sellingPriceText__UZF0W")

        final_price_amount = None
        if len(spans) >= 2:
            price_text = spans[1].text  # second span holds the price
            # Clean up non-breaking spaces and other unwanted chars
            final_price_amount = price_text.replace('\xa0', ' ').strip()

        data.append(final_price_amount)

        # Extract key-value attributes shown in pairs
        attributes = {}
        sections = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'hcl-flex--container') and contains(@class, 'hcl-flex--justify-space-between')]")
        for section in sections:
            try:
                key_element = section.find_element(By.TAG_NAME, "p")
                value_element = section.find_element(By.TAG_NAME, "strong")
                key_text = key_element.text.strip()
                value_text = value_element.text.strip()
                attributes[key_text] = value_text
            except Exception:
                continue
        
        # Append attributes as strings or parse selectively
        for key, val in attributes.items():
            data.append(f"{key}: {val}")
        
        cleaned_data = self.clean_listing_data(data)    
        return cleaned_data
    
    def clean_listing_data(self, raw_data):
        """
        Cleans the raw data list with key:value strings. Strips keys and parses numerical values.
        """
        translation_map = {
            "Pris per kvadratmeter": "Price per square meter",
            "Utgångspris": "Starting price",
            "Prisutveckling": "Price trend",
            "Bostadstyp": "Property type",
            "Upplåtelseform": "Tenure type",
            "Antal rum": "Number of rooms",
            "Boarea": "Living area",
            "Balkong": "Balcony",
            "Våning": "Floor",
            "Byggår": "Year built",
            "Avgift": "Fee",
            "Antal besök": "Number of visits"
        }
        
        raw_data = [d for d in raw_data if d and d.strip() not in ['', ':']]

        def extract_value(cell):
            if cell is None:
                return ''
            if isinstance(cell, float):
                if math.isnan(cell):
                    return ''
                else:
                    return str(cell).strip()
            if not isinstance(cell, str):
                return str(cell).strip()
            if ':' not in cell:
                return cell.strip()
            _, val = cell.split(':', 1)
            return val.strip()
        
        def clean_numeric_value(val):
            if not val:
                return ''
            val_clean = val.replace(' ', '').replace('kr', '').replace('mån', '').replace('rum', '').replace('m²', '').replace(',', '.').strip()
            try:
                # Try float conversion
                if '.' in val_clean:
                    return float(val_clean)
                else:
                    return int(val_clean)
            except:
                return val  # Return original if cannot convert
        
        cleaned = []
        # First two entries are name and price (keep name, clean price numeric)
        cleaned.append(raw_data[0].strip())
        
        # Clean price (final price)
        price_val = extract_value("Final Price: "+ raw_data[1]) if not raw_data[1].startswith('Final Price:') else extract_value(raw_data[1])
        try:
            price_numeric = float(price_val.replace(' ', '').replace('kr','').strip())
            cleaned.append(price_numeric)
        except:
            cleaned.append(price_val)
        
        for item in raw_data[2:]:
            key, sep, val = item.partition(":")
            key_eng = translation_map.get(key, key)
            # Clean numeric values where appropriate
            if key_eng in ["Starting price", "Price trend", "Number of rooms", "Living area", "Fee", "Number of visits", "Year built"]:
                val = clean_numeric_value(val)
            cleaned.append(f"{key_eng}: {val}" if key_eng != '' else val)
        return cleaned

        
    def classify_and_store(self, data):
        if not data or len(data) < 2:
            return
        
        # Try to find "Bostadstyp" (Property type) from attributes
        category = None
        for entry in data:
            entry_str = str(entry)
            if entry_str.startswith("Property type:"):
                category = entry_str.split(":", 1)[1].strip()
                break
        
        if category in self.data:
            self.data[category].append(data)
        else:
            logging.info(f"Ignored listing. Category '{category}' not in allowed list: {data}")


    def scrape(self):
        try:
            for page_url in self.get_all_page_urls():
                try:
                    listing_links = self.get_listing_links(page_url)
                except Exception as e:
                    logging.error(f"Failed to get links for page {page_url}: {e}")
                    continue
                for link in listing_links:
                    try:
                        data = self.extract_listing_data(link)
                        self.classify_and_store(data)
                    except Exception as e:
                        logging.error(f"Failed to extract data from {link}: {e}")
        finally:
            self.driver.quit()

    def save_to_csv(self):
        for category, records in self.data.items():
            if records:
                df = pd.DataFrame(records)
                filename = f"{category}_data.csv"
                logging.info(f"Saving {len(records)} records to {filename}")
                df.to_csv(filename, index=False)


if __name__ == "__main__":
    scraper = HemnetScraper()
    scraper.scrape()
    scraper.save_to_csv()
