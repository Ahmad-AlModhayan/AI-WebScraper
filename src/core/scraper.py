import os
import re
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

    def _extract_tool_details(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        Extract detailed tool information from the page with advanced strategies
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
        
        Returns:
            List[Dict[str, str]]: List of tool details
        """
        tools = []
        
        # Advanced selectors for tool extraction
        tool_selectors = [
            # Specific class-based selectors
            '.ai-tool-card', '.tool-listing', '.ai-tool-item', 
            '.tool-grid-item', '.ai-product-card',
            
            # More generic selectors
            'div[class*="tool"]', 'article[class*="tool"]',
            'div[class*="product"]', 'article[class*="product"]',
            
            # Fallback generic selectors
            'div.card', 'div.item', 'section.tool',
            'div.product', 'article.product'
        ]
        
        # Specific text patterns for tool identification
        tool_keywords = [
            'ai tool', 'web tool', 'productivity tool', 
            'marketing tool', 'ai product', 'web service'
        ]
        
        # Try different selectors
        for selector in tool_selectors:
            tool_elements = soup.select(selector)
            
            if tool_elements:
                for tool in tool_elements:
                    # Advanced name extraction
                    name_selectors = [
                        '.tool-name', '.product-name', 
                        '.ai-tool-title', 'h2', 'h3', 
                        '.card-title', '.item-title'
                    ]
                    name_el = None
                    for name_selector in name_selectors:
                        name_el = tool.select_one(name_selector)
                        if name_el:
                            break
                    
                    # Name extraction with fallback
                    name = name_el.get_text(strip=True) if name_el else None
                    
                    # Advanced description extraction
                    desc_selectors = [
                        '.tool-description', '.product-description', 
                        '.ai-tool-desc', 'p', '.card-text', 
                        '.item-description'
                    ]
                    desc_el = None
                    for desc_selector in desc_selectors:
                        desc_el = tool.select_one(desc_selector)
                        if desc_el:
                            break
                    
                    # Description extraction with fallback
                    description = desc_el.get_text(strip=True) if desc_el else None
                    
                    # Category extraction
                    category_selectors = [
                        '.tool-category', '.product-category', 
                        '.category-tag', '.ai-tool-category'
                    ]
                    category_el = None
                    for cat_selector in category_selectors:
                        category_el = tool.select_one(cat_selector)
                        if category_el:
                            break
                    
                    # Category extraction with fallback
                    category = category_el.get_text(strip=True) if category_el else None
                    
                    # Rating extraction
                    rating_selectors = [
                        '.tool-rating', '.product-rating', 
                        '.rating', '.stars', '.score'
                    ]
                    rating_el = None
                    for rating_selector in rating_selectors:
                        rating_el = tool.select_one(rating_selector)
                        if rating_el:
                            break
                    
                    # Rating extraction with fallback
                    rating = rating_el.get_text(strip=True) if rating_el else None
                    
                    # Validate and enhance tool details
                    if name and description:
                        # Attempt to categorize if not found
                        if not category:
                            # Use keywords to infer category
                            for keyword in tool_keywords:
                                if keyword in name.lower() or keyword in description.lower():
                                    category = keyword.replace('tool', '').replace('ai', '').strip().title()
                                    break
                        
                        # Normalize rating
                        if rating:
                            # Remove non-numeric characters
                            rating = re.sub(r'[^\d.]', '', rating)
                        
                        tools.append({
                            'name': name,
                            'description': description,
                            'category': category or 'Uncategorized',
                            'rating': rating or 'N/A'
                        })
                
                if tools:
                    break  # Stop if we found tools
        
        return tools

    def scrape(self, 
               url: str, 
               max_pages: int = 10, 
               use_proxy: bool = False) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
        """
        Scrape web content with multilingual and configurable support
        
        Args:
            url (str): Target URL to scrape
            max_pages (int): Maximum number of pages to scrape
            use_proxy (bool): Whether to use proxy servers
        
        Returns:
            List[Dict[str, Union[str, List[Dict[str, str]]]]]: Scraped content
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
                
                # Extract tools
                tools = self._extract_tool_details(soup)
                
                # If no tools found, try more aggressive extraction
                if not tools:
                    # Attempt to find text blocks that might represent tools
                    text_blocks = soup.find_all(['div', 'article', 'section'], 
                                                text=re.compile(r'\b(AI|tool|app|service)\b', re.IGNORECASE))
                    
                    for block in text_blocks:
                        name = block.find(['h2', 'h3', 'strong'])
                        desc = block.find('p')
                        
                        if name and desc:
                            tools.append({
                                'name': name.get_text(strip=True),
                                'description': desc.get_text(strip=True),
                                'category': 'Discovered',
                                'rating': 'N/A'
                            })
                
                # Log if still no tools found
                if not tools:
                    logger.warning(f"No tools found on page {current_page} | لم يتم العثور على أدوات في الصفحة {current_page}")
                    break
                
                results.append({
                    'url': url,
                    'page': current_page,
                    'language': self.language,
                    'tools': tools
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
                       results: List[Dict[str, Union[str, List[Dict[str, str]]]]], 
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
        
        # Flatten tools for DataFrame
        flat_results = []
        for result in results:
            for tool in result.get('tools', []):
                flat_tool = tool.copy()
                flat_tool['url'] = result['url']
                flat_tool['page'] = result['page']
                flat_tool['language'] = result['language']
                flat_results.append(flat_tool)
        
        # Convert to DataFrame
        df = pd.DataFrame(flat_results)
        
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
