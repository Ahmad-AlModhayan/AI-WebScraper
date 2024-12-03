import os
import time
import random
import requests
from typing import Dict, List, Optional, Union
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from src.utils.config import config
from src.utils.logging import logger

class WebScraper:
    def __init__(self, 
                 timeout: Optional[int] = None, 
                 language: Optional[str] = None):
        """
        Initialize WebScraper with configurable settings
        
        Args:
            timeout (Optional[int]): Request timeout in seconds
            language (Optional[str]): Language context for scraping
        """
        # Get configuration values with fallback
        self.timeout = timeout or config.get('scraper.default_timeout', 45)
        self.language = language or config.get('app.languages.default', 'ar')
        
        # Scraper configuration
        self.max_retries = config.get('scraper.max_retries', 3)
        self.wait_time = config.get('scraper.wait_time', 5)
        
        # User agent rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        # Proxy configuration
        self.proxies = config.get('scraper.proxies', [])

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate headers for web request with language and user agent support
        
        Returns:
            Dict[str, str]: Request headers
        """
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept-Language': 'ar,en;q=0.9' if self.language == 'ar' else 'en,ar;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        return headers

    def _select_proxy(self) -> Optional[Dict[str, str]]:
        """
        Select a proxy for the request
        
        Returns:
            Optional[Dict[str, str]]: Proxy configuration or None
        """
        if not self.proxies:
            return None
        return {'http': random.choice(self.proxies), 
                'https': random.choice(self.proxies)}

    def scrape(self, 
               url: str, 
               max_pages: int = 10, 
               use_proxy: bool = False) -> List[Dict[str, Union[str, List[str]]]]:
        """
        Scrape web content with multilingual and configurable support
        
        Args:
            url (str): Target URL to scrape
            max_pages (int): Maximum number of pages to scrape
            use_proxy (bool): Whether to use proxy servers
        
        Returns:
            List[Dict[str, Union[str, List[str]]]]: Scraped content
        """
        # Logging in multilingual context
        logger.info(f"Starting scraping for {url} | اِبدأ استخراج المحتوى من {url}")
        
        results = []
        current_page = 1
        
        while current_page <= max_pages:
            try:
                # Prepare request parameters
                headers = self._get_headers()
                proxies = self._select_proxy() if use_proxy else None
                
                # Send request
                response = requests.get(
                    url, 
                    headers=headers, 
                    proxies=proxies, 
                    timeout=self.timeout
                )
                
                # Check response
                response.raise_for_status()
                
                # Parse content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract content based on language
                if self.language == 'ar':
                    content_selectors = [
                        'article', '.article-content', '.entry-content', 
                        'div.content', 'main', 'body'
                    ]
                else:
                    content_selectors = [
                        'article', '.content', '.entry-content', 
                        'div.main-content', 'main', 'body'
                    ]
                
                # Find content
                content_element = None
                for selector in content_selectors:
                    content_element = soup.select_one(selector)
                    if content_element:
                        break
                
                # Extract text
                if content_element:
                    paragraphs = content_element.find_all(['p', 'h1', 'h2', 'h3'])
                    page_content = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                    
                    results.append({
                        'url': url,
                        'page': current_page,
                        'language': self.language,
                        'content': page_content
                    })
                
                # Find next page link
                next_page_link = soup.find('a', text=['Next', 'التالي', 'Next Page', 'الصفحة التالية'])
                if not next_page_link:
                    break
                
                url = next_page_link.get('href')
                current_page += 1
                
                # Wait between requests
                time.sleep(self.wait_time)
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Scraping error: {e} | خطأ في استخراج المحتوى: {e}")
                break
        
        return results

    def export_results(self, 
                       results: List[Dict[str, Union[str, List[str]]]], 
                       format: str = 'json') -> str:
        """
        Export scraping results in various formats
        
        Args:
            results (List[Dict]): Scraped content
            format (str): Export format (json, csv, excel, parquet)
        
        Returns:
            str: Path to exported file
        """
        # Ensure export directory exists
        export_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # Generate filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        base_filename = f'scrape_results_{timestamp}'
        
        # Export based on format
        if format == 'json':
            filepath = os.path.join(export_dir, f'{base_filename}.json')
            df.to_json(filepath, orient='records', force_ascii=False)
        elif format == 'csv':
            filepath = os.path.join(export_dir, f'{base_filename}.csv')
            df.to_csv(filepath, index=False, encoding='utf-8')
        elif format == 'excel':
            filepath = os.path.join(export_dir, f'{base_filename}.xlsx')
            df.to_excel(filepath, index=False)
        elif format == 'parquet':
            filepath = os.path.join(export_dir, f'{base_filename}.parquet')
            df.to_parquet(filepath)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        return filepath
