import requests
from bs4 import BeautifulSoup
import logging
import re

class PriceTracker:
    logger = logging.getLogger(__name__)

    @classmethod
    def get_extraction_strategy(cls, url):
        strategies = {
            'amazon.in': cls.extract_amazon_price,
            'amzn.in': cls.extract_amazon_price,
            'flipkart.com': cls.extract_flipkart_price,
        }
        domain = cls.extract_domain(url)
        return strategies.get(domain)

    @staticmethod
    def extract_domain(url):
        domain_pattern = r'https?://(?:www\.)?([^/]+)'
        match = re.search(domain_pattern, url)
        return match.group(1) if match else None

    @classmethod
    def fetch_product_price(cls, url):
        cls.logger.info(f"Fetching current price with product URL: {url}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            extraction_strategy = cls.get_extraction_strategy(url)
            if not extraction_strategy:
                cls.logger.error(f"No extraction strategy found for domain: {cls.extract_domain(url)}")
                return None

            price = extraction_strategy(response.text)

            if price and price > 0:
                print(f"Successfully fetched price: ₹{price}")
                cls.logger.info(f"Successfully fetched price: ₹{price}")
                return price
            else:
                print(f"No valid price found for: {url}")
                cls.logger.warning(f"No valid price found for: {url}")

        except requests.RequestException as e:
            print(f"Request error: {e}")
            cls.logger.error(f"Request error: {e}")
            return None

        except Exception as e:
            cls.logger.error(f"Unexpected Error: {e}")
            return None 

    @classmethod
    def extract_amazon_price(cls, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            price_element = soup.select_one('.a-price-whole')
            if price_element:
                price = price_element.get_text(strip=True).replace(',', '')
                return float(price)
        except Exception as e:    
            cls.logger.error(f'Error parsing Amazon price: {e}')
            return None
    
    @classmethod
    def extract_flipkart_price(cls, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            price_element = soup.select_one('.Nx9bqj.CxhGGd')  # Update selector as per Flipkart's structure
            if price_element:
                price = price_element.get_text(strip=True).replace('₹', '').replace(',', '')
                return float(price)
        except Exception as e:
            cls.logger.error(f'Error parsing Flipkart price: {e}')
            return None
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tracker = PriceTracker()
    url = input("Enter the product URL: ")
    tracker.fetch_product_price(url)