import logging
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent

class WebScraper:
    def __init__(self, headless: bool = True):
        """
        Initialize WebScraper with configurable options
        
        :param headless: Run browser in headless mode
        """
        self.logger = logging.getLogger(__name__)
        self.headless = headless
        self.driver = self._setup_driver()
        self.ua = UserAgent()
    
    def _setup_driver(self) -> webdriver.Chrome:
        """
        Setup Chrome WebDriver with custom options
        
        :return: Configured Chrome WebDriver
        """
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Random user agent
        chrome_options.add_argument(f'user-agent={self.ua.random}')
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def scrape(self, 
               url: str, 
               max_pages: int = 5, 
               use_proxy: bool = False) -> pd.DataFrame:
        """
        Scrape website content
        
        :param url: Target website URL
        :param max_pages: Maximum number of pages to scrape
        :param use_proxy: Whether to use proxy
        :return: DataFrame with scraped content
        """
        try:
            self.driver.get(url)
            
            # Scraping logic
            scraped_data = []
            current_page = 1
            
            while current_page <= max_pages:
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Extract text and metadata
                page_data = {
                    'url': self.driver.current_url,
                    'title': soup.title.string if soup.title else 'No Title',
                    'content': soup.get_text(separator=' ', strip=True)
                }
                
                scraped_data.append(page_data)
                
                # Check for pagination or navigate
                try:
                    next_page = self.driver.find_element("xpath", "//a[contains(text(), 'Next')]")
                    next_page.click()
                    current_page += 1
                except Exception as e:
                    self.logger.error(f"Error navigating to next page: {e}")
                    break
            
            return pd.DataFrame(scraped_data)
        
        except Exception as e:
            self.logger.error(f"Scraping error: {e}")
            raise
        finally:
            self.driver.quit()

    def close(self):
        """Close WebDriver session"""
        if self.driver:
            self.driver.quit()
