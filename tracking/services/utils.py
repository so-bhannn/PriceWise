import requests
from ..models import Product,ProductAlert,ProductHistory
from django.core.mail import send_mail
from django.utils import timezone
from bs4 import BeautifulSoup
import logging
import re

class PriceTracker:
    logger=logging.getLogger(__name__)

    @classmethod
    def get_extraction_strategy(cls,url):
        strategies={
            'www.amazon.in':cls.extract_amazon_price,
            'www.flipkart.com':cls.extract_flipkart_price,
        }
        domain=cls.extract_domain
        return strategies.get(domain)

    @staticmethod
    def extract_domain(url):
        domain_pattern=r'https?://(?:www\.)?([^/]+)'
        match=re.search(domain_pattern,url)
        return match.group(1) if match else None

    @classmethod
    def get_product_price(cls,url):        
        cls.logger.info(f"fetching current price with product URL: {url}")
        try:
            header={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
            }

            response=requests.get(url,header=header,timeout=10)
            response.raise_for_status()
            extraction_strategy=cls.get_extraction_strategy(url)
            price=extraction_strategy(response.text)

            if price and price>0:
                cls.logger.info(f"Successfully fetched price:₹{price}")
                return price
            else:
                cls.logger.warning(f"No valid price found for: {url}")

        except requests.RequestException as e:
            cls.logger.error("Request error")
            return None

        except Exception as e:
            cls.logger.error("Unexpected Error")
            return None 

    @classmethod
    def extract_amazon_price(cls,html_content):
        
        soup=BeautifulSoup(html_content,'html.parser')
        try:
            price_element=soup.select_one('a-price-whole').replace(',','')
            if price_element:
                return float(price_element)
        except Exception as e:    
            cls.logger.error(f'Error parsing for Amazon:{e}')
            return None
    
    @classmethod
    def extract_flipkart_price(cls,html_content):
        soup=BeautifulSoup(html_content,'html.parser')
        try:
            price_element=soup.select_one('Nx9bqj CxhGGd').replace('₹','').replace(',','')
            if price_element:
                return float(price_element)
        except Exception as e:
            cls.logger.error(f'Error parsing for Flipkart:{e}')
            return None
        
    